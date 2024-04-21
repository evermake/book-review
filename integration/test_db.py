import os
import sqlite3
import uuid
from typing import Generator

import pytest
import yoyo

import book_review.db.users as dbusers


@pytest.fixture
def connection() -> Generator[sqlite3.Connection, None, None]:
    DB = f"db.test.{uuid.uuid4()}.sqlite3"

    backend = yoyo.get_backend(f"sqlite:///{DB}")
    migrations = yoyo.read_migrations("book_review/migrations/")

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

    conn = sqlite3.connect(DB)

    yield conn

    conn.close()
    os.remove(DB)


def test_users_create_and_find(connection: sqlite3.Connection) -> None:
    repo = dbusers.SQLiteRepository(connection)

    logins = [f"login{i}" for i in range(10)]

    ids: dict[int, str] = {}
    for login in logins:
        id = repo.create_user(login, "hash")
        ids[id] = login

    for id, login in ids.items():
        user = repo.find_user(id)

        assert user is not None
        assert user.id == id
        assert user.login == login


def test_users_not_found(connection: sqlite3.Connection) -> None:
    repo = dbusers.SQLiteRepository(connection)

    user = repo.find_user(42)
    assert user is None
