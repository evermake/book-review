import sqlite3
from typing import Callable

import yoyo

ConnectionSupplier = Callable[[], sqlite3.Connection]


def in_memory_connection_supplier() -> sqlite3.Connection:
    return sqlite3.connect(":memory:")


def apply_migrations(db: str) -> None:
    backend = yoyo.get_backend(db)
    migrations = yoyo.read_migrations("book_review/migrations/")

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
