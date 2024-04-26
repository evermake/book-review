from abc import abstractmethod
from datetime import datetime
from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

import book_review.models.reviews as models
from book_review.db import TableReviews


class Review(BaseModel):
    """
    A review in the repository
    """

    user_id: int
    book_id: str
    rating: int
    commentary: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    @classmethod
    def parse_scalar(cls, scalar: TableReviews) -> "Review":
        return Review(
            user_id=scalar.user_id,
            book_id=scalar.book_id,
            rating=scalar.rating,
            commentary=scalar.commentary,
            created_at=scalar.created_at,
            updated_at=scalar.updated_at,
        )

    def map(self) -> models.Review:
        return models.Review(
            user_id=self.user_id,
            book_id=self.book_id,
            rating=self.rating,
            commentary=self.commentary,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class Repository:
    @abstractmethod
    async def delete_review(self, *, user_id: int, book_id: str) -> None:
        """
        Delete a review.
        """
        pass

    @abstractmethod
    async def create_or_update_review(
        self,
        *,
        user_id: int,
        book_id: str,
        rating: int,
        commentary: Optional[str] = None,
    ) -> None:
        """
        Create or update review.
        If the (user_id, book_id) does not exists a new review will be created.
        Otherwise, rating and commentary will be overwritten.
        """
        pass

    @abstractmethod
    async def find_reviews(
        self, *, book_id: Optional[str] = None, user_id: Optional[int] = None
    ) -> Sequence[Review]:
        pass


class ORMRepository(Repository):
    _session: async_sessionmaker[AsyncSession]

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        super().__init__()

        self._session = session_maker

    async def delete_review(self, *, user_id: int, book_id: str) -> None:
        statement = (
            delete(TableReviews)
            .where(TableReviews.user_id == user_id)
            .where(TableReviews.book_id == book_id)
        )

        async with self._session() as session:
            async with session.begin():
                await session.execute(statement)

    async def create_or_update_review(
        self,
        *,
        user_id: int,
        book_id: str,
        rating: int,
        commentary: Optional[str] = None,
    ) -> None:
        """
        Create or update review.
        If the (user_id, book_id) does not exists a new review will be created.
        Otherwise, rating and commentary will be overwritten.
        """

        statement = insert(TableReviews).values(
            user_id=user_id, book_id=book_id, rating=rating, commentary=commentary
        )

        statement = statement.on_conflict_do_update(
            index_elements=[TableReviews.user_id, TableReviews.book_id],
            set_={
                TableReviews.rating: statement.excluded.rating,
                TableReviews.commentary: statement.excluded.commentary,
                TableReviews.updated_at: datetime.now(),
            },
        )

        async with self._session() as session:
            async with session.begin():
                await session.execute(statement)

    async def find_reviews(
        self, *, book_id: Optional[str] = None, user_id: Optional[int] = None
    ) -> Sequence[Review]:
        statement = select(TableReviews)

        if book_id is not None:
            statement = statement.where(TableReviews.book_id == book_id)

        if user_id is not None:
            statement = statement.where(TableReviews.user_id == user_id)

        async with self._session() as session:
            reviews = await session.scalars(statement)

            return list(map(Review.parse_scalar, reviews))
