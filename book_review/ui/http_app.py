from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

from book_review.config import settings
from book_review.models.user import User
from book_review.usecase.openlibrary import UseCase as OpenlibraryUseCase
from book_review.usecase.reviews import UseCase as ReviewsUseCase
from book_review.usecase.users import UseCase as UsersUseCase

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

        config = uvicorn.Config(self._app, port=settings.PORT, log_level="info")
        server = uvicorn.Server(config)

        await server.serve()

    def _register_routes(self) -> None:
        app = self._app

        @app.get("/ping", response_model=str)
        async def ping() -> str:
            return "pong"

        @app.post("/token")
        async def token(
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        ) -> Token:
            user = self._users.authenticate_user(form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            access_token_expires = timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

            access_token = self._create_access_token(
                data={"sub": user.login}, expires_delta=access_token_expires
            )

            return Token(access_token=access_token, token_type="bearer")

        @app.get("/users/me/", response_model=User)
        async def users_me(
            user: Annotated[User, Depends(self._get_user)],
        ):
            return user

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

        return user

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
