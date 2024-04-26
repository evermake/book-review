from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

import book_review.models.user as models
from book_review.db import TableUsers

UserID = models.UserID


class User(BaseModel):
    """
    A user in the repository.
    """

    id: UserID
    login: str
    password_hash: str
    created_at: datetime

    @classmethod
    def parse_scalar(cls, scalar: TableUsers) -> "User":
        return cls(
            id=scalar.id,
            login=scalar.login,
            password_hash=scalar.password_hash,
            created_at=scalar.created_at,
        )

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


class ORMRepository(Repository):
    _session: async_sessionmaker[AsyncSession]

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        super().__init__()

        self._session = session_maker

    async def find_users(self, *, login_like: Optional[str] = None) -> Sequence[User]:
        """
        Find users by the login substring.
        If the login is not provided it will return all users.
        """

        statement = select(TableUsers)

        if login_like is not None:
            statement = statement.where(TableUsers.login.like(login_like))

        async with self._session() as session:
            users = await session.scalars(statement)

            return list(map(User.parse_scalar, users))

    async def find_user_by_id(self, id: UserID) -> Optional[User]:
        statement = select(TableUsers).where(TableUsers.id == id)

        async with self._session() as session:
            user = await session.scalar(statement)

            if user is None:
                return None

            return User.parse_scalar(user)

    async def find_user_by_login(self, login: str) -> Optional[User]:
        statement = select(TableUsers).where(TableUsers.login == login)

        async with self._session() as session:
            user = await session.scalar(statement)

            if user is None:
                return None

            return User.parse_scalar(user)

    async def create_user(self, login: str, password_hash: str) -> int:
        statement = (
            insert(TableUsers)
            .values(login=login, password_hash=password_hash)
            .returning(TableUsers.id)
        )

        async with self._session() as session:
            async with session.begin():
                result = await session.execute(statement)

                id = result.scalar_one()

                return id
