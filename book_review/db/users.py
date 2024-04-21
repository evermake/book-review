import sqlite3
from abc import abstractmethod

from pydantic import BaseModel

import book_review.db.repository as db


class User(BaseModel):
    id: int
    login: str
    password_hash: str
    created_at: sqlite3.Timestamp


class Repository(db.Repository):
    @abstractmethod
    def find_user(self, id: int) -> User:
        pass

    @abstractmethod
    def create_user(self, login: str, password_hash: str) -> int:
        pass


class SQLiteRepository(Repository):
    connection: sqlite3.Connection

    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__()

        self.connection = connection

    @staticmethod
    def connect(database: str) -> "SQLiteRepository":
        return SQLiteRepository(sqlite3.connect(database))

    @staticmethod
    def in_memory() -> "SQLiteRepository":
        return SQLiteRepository.connect(":memory:")

    def close(self) -> None:
        self.connection.close()

    def find_user(self, id: int) -> User:
        cursor = self.connection.execute(
            "SELECT id, login, password_hash, created_at FROM users u WHERE u.id = ?",
            (id,),
        )
        row = cursor.fetchone()

        (id, login, password_hash, created_at) = row

        return User(
            id=id, login=login, password_hash=password_hash, created_at=created_at
        )

    def create_user(self, login: str, password_hash: str) -> int:
        cursor = self.connection.execute(
            "INSERT INTO users (login, password_hash) VALUES (?, ?) RETURNING id",
            (login, password_hash),
        )

        row = cursor.fetchone()

        self.connection.commit()

        (id,) = row

        return int(id)
