from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Annotated, Any, AsyncGenerator, Optional, Sequence

import orjson
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.coder import Coder
from fastapi_cache.decorator import cache
from jose import JWTError, jwt
from pydantic import BaseModel

from book_review.config import settings
from book_review.models.book import CoverID
from book_review.usecase.openlibrary import UseCase as OpenlibraryUseCase
from book_review.usecase.reviews import UseCase as ReviewsUseCase
from book_review.usecase.users import UseCase as UsersUseCase

from .models import (
    Book,
    BookID,
    BookPreview,
    CoverSize,
    Review,
    ReviewRequest,
    User,
    UserID,
)

_OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")


class _Tags(str, Enum):
    REVIEWS = "reviews"
    BOOKS = "books"
    USERS = "users"
    HEALTHCHECK = "healthcheck"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login: str


class ORJSONCoder(Coder):
    @classmethod
    def encode(cls, value: Any) -> str:
        return orjson.dumps(
            value,
            default=jsonable_encoder,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY,
        ).decode()

    @classmethod
    def decode(cls, value: str) -> Any:
        return orjson.loads(value)


class App:
    _app: FastAPI

    _users: UsersUseCase
    _reviews: ReviewsUseCase
    _openlibrary: OpenlibraryUseCase

    def __init__(
        self,
        *,
        users: UsersUseCase,
        reviews: ReviewsUseCase,
        openlibrary: OpenlibraryUseCase,
        title: str = "Book Review Platform",
        summary: str = """
        BRP is a dynamic online platform designed to foster a vibrant community of book
        lovers, where they can share their thoughts, discover new reads, and engage in
        meaningful discussions. With a user-friendly interface and seamless integration
        of external APIs, BRP offers an immersive experience for bibliophiles.
        """,
        description: str = "",
        version: str = "0.1.0",
    ) -> None:
        @asynccontextmanager
        async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
            FastAPICache.init(InMemoryBackend(), coder=ORJSONCoder)

            yield

        self._app = FastAPI(
            debug=settings.DEBUG,
            title=title,
            summary=summary,
            description=description,
            version=version,
            lifespan=lifespan,
            default_response_class=ORJSONResponse,
        )

        self._users = users
        self._reviews = reviews
        self._openlibrary = openlibrary

    async def serve(self) -> None:
        self._register_routes()

        log_level = "debug" if settings.DEBUG else "info"

        config = uvicorn.Config(self._app, port=settings.PORT, log_level=log_level)
        server = uvicorn.Server(config)

        await server.serve()

    def _register_routes(self) -> None:
        app = self._app

        @app.get("/health", tags=[_Tags.HEALTHCHECK.value])
        async def health() -> str:
            return "ok"

        @app.post("/token", tags=[_Tags.USERS.value])
        async def token(
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        ) -> Token:
            user = await self._users.authenticate_user(
                form_data.username, form_data.password
            )

            if not user:
                # TODO: add this exception into schema
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            access_token_expires = timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

            access_token = self._create_access_token(
                data={"sub": user.login}, expires_delta=access_token_expires
            )

            return Token(access_token=access_token, token_type="bearer")

        @app.get("/books", tags=[_Tags.BOOKS.value])
        @cache(expire=60 * 60 * 24)
        async def search_books(query: str) -> Sequence[BookPreview]:
            books = await self._openlibrary.search_books_previews(query)

            return list(map(BookPreview.parse, books))

        @app.get("/books/{id}", tags=[_Tags.BOOKS.value])
        @cache(expire=60 * 60 * 24)
        async def get_book(id: BookID) -> Book:
            book = await self._openlibrary.get_book(id)

            if book is None:
                # TODO: add this exception into schema
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"book with id {repr(id)} not found",
                )

            return Book.parse(book)

        @app.get(
            "/covers/{id}",
            responses={200: {"content": {"image/jpeg": {}}}},
            # Prevent FastAPI from adding "application/json" as an additional
            # response media type in the autogenerated OpenAPI specification.
            # https://github.com/tiangolo/fastapi/issues/3258
            response_class=Response,
            tags=[_Tags.BOOKS.value],
        )
        @cache(expire=60 * 60 * 24)
        async def get_cover(id: CoverID, size: CoverSize = CoverSize.SMALL) -> Response:
            cover = await self._openlibrary.get_cover(
                id,
                size,
            )

            if cover is None:
                # TODO: add this exception into schema
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"image with id {repr(id)} not found",
                )

            return Response(cover, media_type="image/jpeg")

        @app.post(
            "/reviews", tags=[_Tags.REVIEWS.value, _Tags.BOOKS.value, _Tags.USERS.value]
        )
        async def create_or_update_review(
            user: Annotated[User, Depends(self._get_user)], review: ReviewRequest
        ) -> None:
            await self._reviews.create_or_update_review(
                user_id=user.id,
                book_id=review.book_id,
                rating=review.rating,
                commentary=review.commentary,
            )

        @app.delete(
            "/reviews", tags=[_Tags.BOOKS.value, _Tags.REVIEWS.value, _Tags.USERS.value]
        )
        async def delete_review(
            user: Annotated[User, Depends(self._get_user)], book_id: BookID
        ) -> None:
            await self._reviews.delete_review(user_id=user.id, book_id=book_id)

        @app.get(
            "/reviews", tags=[_Tags.BOOKS.value, _Tags.REVIEWS.value, _Tags.USERS.value]
        )
        @cache(5)
        async def find_reviews(
            book_id: Optional[BookID] = None,
            user_id: Optional[UserID] = None,
        ) -> Sequence[Review]:
            reviews = await self._reviews.find_reviews(book_id, user_id)

            return list(map(Review.parse, reviews))

        @app.post("/users", tags=[_Tags.USERS.value])
        async def create_user(login: str, password: str) -> User:
            user = await self._users.find_user_by_login(login)
            if user is not None:
                # TODO: add this exception into schema
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"user {repr(login)} exists",
                )

            id = await self._users.create_user(login, password)
            user = await self._users.find_user_by_id(id)

            if user is None:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return User(id=user.id, login=user.login, created_at=user.created_at)

        @app.get("/users", tags=[_Tags.USERS.value])
        @cache(20)
        async def get_users(login: Optional[str] = None) -> Sequence[User]:
            users = await self._users.find_users(login=login)

            return list(map(User.parse, users))

        @app.get("/users/single", tags=[_Tags.USERS.value])
        @cache(20)
        async def get_single_user(
            id: Optional[UserID] = None, login: Optional[str] = None
        ) -> User:
            if id is not None:
                user = await self._users.find_user_by_id(id)

                if user is None:
                    # TODO: add this exception into schema
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"user with id {id:r} not found",
                    )

                return User.parse(user)

            if login is not None:
                user = await self._users.find_user_by_login(login)

                if user is None:
                    # TODO: add this exception into schema
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"user with login {login:r} not found",
                    )

                return User.parse(user)

            # TODO: add this exception into schema
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="either id or login is required",
            )

        @app.get("/users/me", tags=[_Tags.USERS.value])
        @cache(5)
        async def get_current_user(
            user: Annotated[User, Depends(self._get_user)],
        ) -> User:
            return user

        @app.get("/users/me/reviews", tags=[_Tags.USERS.value, _Tags.REVIEWS.value])
        @cache(5)
        async def get_current_user_reviews(
            user: Annotated[User, Depends(self._get_user)],
        ) -> Sequence[Review]:
            reviews = await self._reviews.find_reviews(user_id=user.id)

            return list(map(Review.parse, reviews))

    async def _get_user(self, token: Annotated[str, Depends(_OAUTH2_SCHEME)]) -> User:
        # TODO: add this exception into schema
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )

            login: Optional[str] = payload.get("sub")

            if login is None:
                raise credentials_exception

            token_data = TokenData(login=login)
        except JWTError:
            raise credentials_exception

        user = await self._users.find_user_by_login(token_data.login)

        if user is None:
            raise credentials_exception

        return User.parse(user)

    def _create_access_token(
        self, data: dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        if expires_delta is None:
            expires_delta = timedelta(minutes=15)

        to_encode = data.copy()

        expires_at = datetime.now(timezone.utc) + expires_delta

        to_encode.update({"exp": expires_at})

        encoded_jwt: str = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

        return encoded_jwt
