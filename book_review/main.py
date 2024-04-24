import asyncio
import sqlite3
import sys

import rich.traceback
import uvloop

import book_review.db.repository as db
from book_review.config import settings
from book_review.db.reviews import SQLiteRepository as ReviewsRepository
from book_review.db.users import SQLiteRepository as UsersRepository
from book_review.openlibrary.client import HTTPAPIClient as OpenlibraryClient
from book_review.ui.http_app import App
from book_review.usecase.openlibrary import UseCase as OpenlibraryUseCase
from book_review.usecase.reviews import UseCase as ReviewsUseCase
from book_review.usecase.users import UseCase as UsersUseCase


def get_database_connection_supplier() -> db.ConnectionSupplier:
    db.apply_migrations(f"sqlite:///{settings.DB}")

    return lambda: sqlite3.connect(settings.DB)


async def run() -> None:
    connection_supplier = get_database_connection_supplier()

    app = App(
        users=UsersUseCase(UsersRepository(connection_supplier)),
        reviews=ReviewsUseCase(ReviewsRepository(connection_supplier)),
        openlibrary=OpenlibraryUseCase(OpenlibraryClient()),
    )

    await app.serve()


def main() -> None:
    rich.traceback.install()

    if sys.version_info >= (3, 11):
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(run())
    else:
        uvloop.install()
        asyncio.run(main())


if __name__ == "__main__":
    main()
