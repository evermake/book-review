from typing import Optional
import book_review.repository.repository as repository

from pydantic import BaseModel
from datetime import datetime

import sqlite3


class User(BaseModel):
    id: int
    login: str
    password_hash: str
    created_at: datetime


class Repository(repository.Repository):
    connection: sqlite3.Connection

    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__()

        self.connection = connection

    @staticmethod
    def connect(database: str) -> "Repository":
        return Repository(sqlite3.connect(database))

    @staticmethod
    def in_memory() -> "Repository":
        return Repository.connect(":memory:")

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

        row = cursor.fetchone()

        if not row:
            return None

        (id,) = row[0]

        return int(id)
