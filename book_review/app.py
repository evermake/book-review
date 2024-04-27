from typing import Any

import orjson
import sqlalchemy.ext.asyncio as sqlalchemy
from aiohttp import ClientSession
from yarl import URL

import book_review.db as db
from book_review.config import settings
from book_review.controller.http.app import App as HTTPApp
from book_review.dao.reviews import ORMRepository as ReviewsRepository
from book_review.dao.users import ORMRepository as UsersRepository
from book_review.openlibrary.client import HTTPAPIClient as OpenlibraryClient
from book_review.usecase.openlibrary import UseCase as OpenlibraryUseCase
from book_review.usecase.reviews import UseCase as ReviewsUseCase
from book_review.usecase.users import UseCase as UsersUseCase


def _create_http_client_session(base_url: URL) -> ClientSession:
    def encoder(value: Any) -> str:
        return orjson.dumps(value).decode()

    return ClientSession(base_url, json_serialize=encoder)


def _create_db_engine() -> sqlalchemy.AsyncEngine:
    return sqlalchemy.create_async_engine(
        f"sqlite+aiosqlite:///{settings.DB}", echo=settings.DEBUG
    )


def _create_db_session_maker(
    engine: sqlalchemy.AsyncEngine,
) -> sqlalchemy.async_sessionmaker[sqlalchemy.AsyncSession]:
    return sqlalchemy.async_sessionmaker(engine)


async def run() -> None:
    """
    Setup and run the app.
    """

    db_engine = _create_db_engine()

    # migrations
    await db.create_all(db_engine)

    session_maker = _create_db_session_maker(db_engine)

    http_app = HTTPApp(
        users=UsersUseCase(UsersRepository(session_maker)),
        reviews=ReviewsUseCase(ReviewsRepository(session_maker)),
        openlibrary=OpenlibraryUseCase(
            OpenlibraryClient(
                api_session=_create_http_client_session(
                    URL(settings.OPENLIBRARY_BASE_URL)
                ),
                covers_session=_create_http_client_session(
                    URL(settings.OPENLIBRARY_COVERS_BASE_URL)
                ),
            )
        ),
    )

    await http_app.serve()
