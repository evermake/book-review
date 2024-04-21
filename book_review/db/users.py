import sqlite3
from abc import abstractmethod
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

import book_review.db.repository as db


class User(BaseModel):
    id: int
    login: str
    password_hash: str
    created_at: datetime


class Repository(db.Repository):
    @abstractmethod
    def find_user(self, id: int) -> list[User]:
        pass

    @abstractmethod
    def create_user(self, login: str, password_hash: str) -> Optional[int]:
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

    def find_user(self, id: int) -> list[User]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, login, password_hash, created_at FROM users u WHERE u.id = ?",
            (id,),
        )
        rows = cursor.fetchall()

        users: list[User] = []

        for row in rows:
            (id, login, password_hash, created_at) = row

            user = User(
                id=id, login=login, password_hash=password_hash, created_at=created_at
            )

            users.append(user)

        return users

    def create_user(self, login: str, password_hash: str) -> Optional[int]:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO users (login, password_hash) VALUES (?, ?) RETURNING id",
            (login, password_hash),
        )
        self.connection.commit()

        row = cursor.fetchone()

        if not row:
            return None

        (id,) = row[0]

        return int(id)
