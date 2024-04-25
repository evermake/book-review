from typing import Callable

import aiosqlite
import yoyo

ConnectionSupplier = Callable[[], aiosqlite.Connection]


def in_memory_connection_supplier() -> aiosqlite.Connection:
    return aiosqlite.connect(":memory:")


def apply_migrations(db: str) -> None:
    backend = yoyo.get_backend(db)
    migrations = yoyo.read_migrations("book_review/migrations/")

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
