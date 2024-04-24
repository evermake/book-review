import uvicorn
from fastapi import FastAPI

from book_review.config import settings
from book_review.usecase.openlibrary import UseCase as OpenlibraryUseCase
from book_review.usecase.reviews import UseCase as ReviewsUseCase
from book_review.usecase.users import UseCase as UsersUseCase


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
        def ping() -> str:
            return "pong"
