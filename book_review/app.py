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


def _get_client_session(base_url: URL) -> ClientSession:
    def encoder(value: Any) -> str:
        return orjson.dumps(value).decode()

    return ClientSession(base_url, json_serialize=encoder)


def _create_engine() -> sqlalchemy.AsyncEngine:
    return sqlalchemy.create_async_engine(
        f"sqlite+aiosqlite:///{settings.DB}", echo=settings.DEBUG
    )


def _get_session_maker(
    engine: sqlalchemy.AsyncEngine,
) -> sqlalchemy.async_sessionmaker[sqlalchemy.AsyncSession]:
    return sqlalchemy.async_sessionmaker(engine)


class App:
    _engine: sqlalchemy.AsyncEngine

    # TODO: improve setup
    async def _setup(self) -> None:
        self._engine = _create_engine()

        await self._setup_db()

    async def _setup_db(self) -> None:
        await db.create_all(self._engine)

    async def _serve_http_app(self) -> None:
        session_maker = _get_session_maker(self._engine)

        http_app = HTTPApp(
            users=UsersUseCase(UsersRepository(session_maker)),
            reviews=ReviewsUseCase(ReviewsRepository(session_maker)),
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

        await self._setup()
        await self._serve_http_app()
