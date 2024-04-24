import asyncio
import sqlite3
import sys

import rich.traceback
import uvloop

from book_review.db.reviews import SQLiteRepository as ReviewsRepository
from book_review.db.users import SQLiteRepository as UsersRepository
from book_review.openlibrary.client import HTTPAPIClient as OpenlibraryClient
from book_review.ui.http_app import App
from book_review.usecase.openlibrary import UseCase as OpenlibraryUseCase
from book_review.usecase.reviews import UseCase as ReviewsUseCase
from book_review.usecase.users import UseCase as UsersUseCase


def get_db_connection() -> sqlite3.Connection:
    return sqlite3.connect("db.sqlite3")


async def run() -> None:
    connection = get_db_connection()

    app = App(
        users=UsersUseCase(UsersRepository(connection)),
        reviews=ReviewsUseCase(ReviewsRepository(connection)),
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
