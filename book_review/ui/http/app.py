from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Optional, Sequence

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login: str


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
    ) -> None:
        self._app = FastAPI(debug=settings.DEBUG)

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

        @app.get("/health", tags=["healthcheck"])
        async def health() -> str:
            return "ok"

        @app.post("/token")
        async def token(
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        ) -> Token:
            user = self._users.authenticate_user(form_data.username, form_data.password)
            if not user:
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

        @app.get("/books", tags=["books"])
        async def search_books(query: str) -> Sequence[BookPreview]:
            books = await self._openlibrary.search_books_previews(query)

            return list(map(lambda b: BookPreview.parse(b), books))

        @app.get("/books/{id}", tags=["books"])
        async def get_book(id: BookID) -> Book:
            book = await self._openlibrary.get_book(id)

            if book is None:
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
            tags=["books"],
        )
        async def get_cover(id: CoverID, size: CoverSize = CoverSize.Small) -> Response:
            cover = await self._openlibrary.get_cover(
                id,
                size,
            )

            if cover is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"image with id {repr(id)} not found",
                )

            return Response(cover, media_type="image/jpeg")

        @app.post("/reviews", tags=["reviews", "books"])
        async def create_or_update_review(
            user: Annotated[User, Depends(self._get_user)], review: ReviewRequest
        ) -> None:
            self._reviews.create_or_update_review(
                user_id=user.id,
                book_id=review.book_id,
                rating=review.rating,
                commentary=review.commentary,
            )

        @app.get("/reviews", tags=["reviews", "books", "users"])
        async def find_reviews(
            book_id: Optional[BookID] = None,
            user_id: Optional[UserID] = None,
        ) -> Sequence[Review]:
            reviews = self._reviews.find_reviews(book_id, user_id)

            return list(map(lambda r: Review.parse(r), reviews))

        @app.post("/users", tags=["users"])
        async def create_user(login: str, password: str) -> User:
            id = self._users.create_user(login, password)

            user = self._users.find_user_by_id(id)

            if user is None:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return User(id=user.id, login=user.login, created_at=user.created_at)

        @app.get("/users", tags=["users"])
        async def get_users(login: Optional[str] = None) -> Sequence[User]:
            users = self._users.find_users(login=login)

            return list(map(lambda u: User.parse(u), users))

        @app.get("/users/single", tags=["users"])
        async def get_single_user(
            id: Optional[UserID] = None, login: Optional[str] = None
        ) -> User:
            if id is not None:
                user = self._users.find_user_by_id(id)

                if user is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"user with id {id:r} not found",
                    )

                return User.parse(user)

            if login is not None:
                user = self._users.find_user_by_login(login)

                if user is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"user with login {login:r} not found",
                    )

                return User.parse(user)

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="either id or login is required",
            )

        @app.get("/users/me", tags=["users"])
        async def get_current_user(
            user: Annotated[User, Depends(self._get_user)],
        ) -> User:
            return user

        @app.get("/users/me/reviews", tags=["users", "reviews"])
        async def get_current_user_reviews(
            user: Annotated[User, Depends(self._get_user)],
        ) -> Sequence[Review]:
            reviews = self._reviews.find_reviews(user_id=user.id)

            return list(map(lambda r: Review.parse(r), reviews))

    def _get_user(self, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
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

        user = self._users.find_user_by_login(token_data.login)

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
