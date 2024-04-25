import os.path
import sqlite3

import rich.traceback
from aiohttp import ClientSession
from aiohttp_client_cache.backends.base import CacheBackend
from aiohttp_client_cache.backends.sqlite import SQLiteBackend
from aiohttp_client_cache.session import CachedSession
from yarl import URL

import book_review.db.repository as db
from book_review.config import settings
from book_review.db.reviews import SQLiteRepository as ReviewsRepository
from book_review.db.users import SQLiteRepository as UsersRepository
from book_review.openlibrary.client import HTTPAPIClient as OpenlibraryClient
from book_review.ui.http.app import App as HTTPApp
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


def _get_database_connection_supplier() -> db.ConnectionSupplier:
    return lambda: sqlite3.connect(settings.DB)


def _get_cache_backend() -> CacheBackend:
    return SQLiteBackend(expire_after=settings.CACHE_EXPIRE_MINUTES, autoclose=True)


def _get_aiohttp_client_session(base_url: URL, *, cache: bool = False) -> ClientSession:
    if cache:
        session: ClientSession = CachedSession(base_url, cache=_get_cache_backend())
        return session

    return ClientSession(base_url)


async def _serve_http_app() -> None:
    connection_supplier = _get_database_connection_supplier()

    app = HTTPApp(
        users=UsersUseCase(UsersRepository(connection_supplier)),
        reviews=ReviewsUseCase(ReviewsRepository(connection_supplier)),
        openlibrary=OpenlibraryUseCase(
            OpenlibraryClient(
                api_session=_get_aiohttp_client_session(
                    URL(settings.OPENLIBRARY_BASE_URL), cache=True
                ),
                covers_session=_get_aiohttp_client_session(
                    URL(settings.OPENLIBRARY_COVERS_BASE_URL)
                ),
            )
        ),
    )

    await app.serve()


class App:
    @staticmethod
    def setup() -> None:
        rich.traceback.install(show_locals=settings.DEBUG)

        _apply_migrations()

    @staticmethod
    async def run() -> None:
        await _serve_http_app()
