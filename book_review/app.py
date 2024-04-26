import os.path
from typing import Any

import orjson
import rich.traceback
from aiohttp import ClientSession
from yarl import URL

import book_review.db as db
from book_review.config import settings
from book_review.controller.http.app import App as HTTPApp
from book_review.db.reviews import SQLiteRepository as ReviewsRepository
from book_review.db.users import SQLiteRepository as UsersRepository
from book_review.openlibrary.client import HTTPAPIClient as OpenlibraryClient
from book_review.usecase.openlibrary import UseCase as OpenlibraryUseCase
from book_review.usecase.reviews import UseCase as ReviewsUseCase
from book_review.usecase.users import UseCase as UsersUseCase


def _apply_migrations() -> None:
    if not os.path.exists(settings.DB):
        open(settings.DB, "a").close()

    if os.path.isabs(settings.DB):
        db.apply_migrations(f"sqlite:///{settings.DB}")
        return

    abs = os.path.abspath(settings.DB)

    db.apply_migrations(f"sqlite:///{abs}")


def _get_db_connection_pool() -> db.ConnectionPool:
    return db.ConnectionPool(settings.DB, max_connections=500)


def _get_client_session(base_url: URL) -> ClientSession:
    def encoder(value: Any) -> str:
        return orjson.dumps(value).decode()

    return ClientSession(base_url, json_serialize=encoder)


class App:
    def setup(self) -> None:
        """
        Setup the application.
        """

        rich.traceback.install(show_locals=settings.DEBUG)

        _apply_migrations()

    async def _serve_http_app(self) -> None:
        pool = _get_db_connection_pool()

        http_app = HTTPApp(
            users=UsersUseCase(UsersRepository(pool)),
            reviews=ReviewsUseCase(ReviewsRepository(pool)),
            openlibrary=OpenlibraryUseCase(
                OpenlibraryClient(
                    api_session=_get_client_session(URL(settings.OPENLIBRARY_BASE_URL)),
                    covers_session=_get_client_session(
                        URL(settings.OPENLIBRARY_COVERS_BASE_URL)
                    ),
                )
            ),
        )

        await http_app.serve()

    async def run(self) -> None:
        """
        Run the app.
        Make sure that the setup was called before running this method.
        """

        await self._serve_http_app()
