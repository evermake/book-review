import sqlite3
from abc import ABC, abstractmethod
from typing import Optional, Sequence

import aiosqlite
from pydantic import BaseModel

import book_review.models.user as models
from book_review.db import ConnectionSupplier, in_memory_connection_supplier

UserID = models.UserID


class UserExistsError(Exception):
    def __init__(self) -> None:
        super().__init__("user exists")


class User(BaseModel):
    """
    A user in the repository.
    """

    id: UserID
    login: str
    password_hash: str
    created_at: sqlite3.Timestamp

    def map(self) -> models.User:
        return models.User(id=self.id, login=self.login, created_at=self.created_at)


class Repository(ABC):
    @abstractmethod
    async def find_users(self, *, login_like: Optional[str] = None) -> Sequence[User]:
        """
        Find users by the login substring.
        If the login is not provided it will return all users.
        """
        pass

    @abstractmethod
    async def find_user_by_id(self, id: UserID) -> Optional[User]:
        pass

    @abstractmethod
    async def find_user_by_login(self, login: str) -> Optional[User]:
        pass

    @abstractmethod
    async def create_user(self, login: str, password_hash: str) -> int:
        pass


class SQLiteRepository(Repository):
    """
    Repository that uses SQLite3 backend.
    """

    _connection_supplier: ConnectionSupplier

    def __init__(self, connection_supplier: ConnectionSupplier) -> None:
        super().__init__()

        self._connection_supplier = connection_supplier

    @classmethod
    def in_memory(cls) -> "SQLiteRepository":
        return cls(in_memory_connection_supplier)

    async def find_users(self, *, login_like: Optional[str] = None) -> Sequence[User]:
        params: dict[str, str] = {}

        if login_like is not None:
            params["login_like"] = login_like

        query = "SELECT id, login, password_hash, created_at FROM users"

        if params:
            statements = ["login LIKE :login_like"]

            query += f" WHERE {' AND '.join(statements)}"

        async with self._connection_supplier() as connection:
            cursor = await connection.execute(query, params)
            rows = await cursor.fetchall()

            users: list[User] = []

            for row in rows:
                (id, login, password_hash, created_at) = row

                assert id is not None
                assert login is not None

                user = User(
                    id=id,
                    login=login,
                    password_hash=password_hash,
                    created_at=created_at,
                )

                users.append(user)

            return users

    async def find_user_by_id(self, id: UserID) -> Optional[User]:
        async with self._connection_supplier() as connection:
            cursor = await connection.execute(
                "SELECT id, login, password_hash, created_at FROM users WHERE id = ?",
                (id,),
            )

            return await self._fetch_user(cursor)

    async def find_user_by_login(self, login: str) -> Optional[User]:
        async with self._connection_supplier() as connection:
            cursor = await connection.execute(
                "SELECT id, login, password_hash, created_at FROM users WHERE login = ?",
                (login,),
            )

            return await self._fetch_user(cursor)

    async def _fetch_user(self, cursor: aiosqlite.Cursor) -> Optional[User]:
        row = await cursor.fetchone()

        if row is None:
            return None

        (id, login, password_hash, created_at) = row

        return User(
            id=id, login=login, password_hash=password_hash, created_at=created_at
        )

    async def create_user(self, login: str, password_hash: str) -> int:
        async with self._connection_supplier() as connection:
            try:
                cursor = await connection.execute(
                    "INSERT INTO users (login, password_hash) VALUES (?, ?) RETURNING id",
                    (login, password_hash),
                )

                row = await cursor.fetchone()

                assert row is not None

                (id,) = row

                return int(id)
            except sqlite3.IntegrityError:
                raise UserExistsError()
