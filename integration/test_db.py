import os
import sqlite3
from typing import Generator

import pytest
import yoyo

import book_review.db.users as dbusers

DB = "db.test.sqlite3"


@pytest.fixture(autouse=True, scope="session")
def connection() -> Generator[sqlite3.Connection, None, None]:
    backend = yoyo.get_backend(f"sqlite:///{DB}")
    migrations = yoyo.read_migrations("book_review/migrations/")

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

    conn = sqlite3.connect(DB)

    yield conn

    conn.close()
    os.remove(DB)


def test_create_user(connection: sqlite3.Connection) -> None:
    repo = dbusers.SQLiteRepository(connection)

    logins = [f"login{i}" for i in range(10)]

    ids: dict[int, str] = {}
    for login in logins:
        id = repo.create_user(login, "hash")
        ids[id] = login

    for id, login in ids.items():
        user = repo.find_user(id)

        assert user.id == id
        assert user.login == login
