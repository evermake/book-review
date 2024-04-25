import sqlite3
from abc import abstractmethod
from typing import Optional, Sequence

from pydantic import BaseModel

import book_review.models.reviews as models
from book_review.db import ConnectionSupplier, in_memory_connection_supplier


class Review(BaseModel):
    """
    A review in the repository
    """

    user_id: int
    book_id: str
    rating: int
    commentary: Optional[str] = None
    created_at: sqlite3.Timestamp
    updated_at: Optional[sqlite3.Timestamp] = None

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
    def delete_review(self, *, user_id: int, book_id: str) -> None:
        """
        Delete a review.
        """
        pass

    @abstractmethod
    def create_or_update_review(
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
    def find_reviews(
        self, *, book_id: Optional[str] = None, user_id: Optional[int] = None
    ) -> Sequence[Review]:
        pass


class SQLiteRepository(Repository):
    """
    Repository that uses SQLite3 backend.
    """

    _connection_supplier: ConnectionSupplier
    _table = "reviews"

    def __init__(self, connection_supplier: ConnectionSupplier) -> None:
        super().__init__()

        self._connection_supplier = connection_supplier

    @classmethod
    def in_memory(cls) -> "SQLiteRepository":
        return cls(in_memory_connection_supplier)

    def find_reviews(
        self, *, book_id: Optional[str] = None, user_id: Optional[int] = None
    ) -> Sequence[Review]:
        query = f"SELECT user_id, book_id, rating, commentary, created_at, updated_at FROM {self._table}"

        params: dict[str, str | int] = dict()

        if book_id is not None:
            params["book_id"] = book_id

        if user_id is not None:
            params["user_id"] = user_id

        if params:
            statements = [f"{col} = :{col}" for col in params.keys()]

            query += f" WHERE {' AND '.join(statements)}"

        with self._connection_supplier() as connection:
            cursor = connection.execute(query, params)
            rows = cursor.fetchall()

            reviews: list[Review] = []

            for row in rows:
                (
                    user_id,
                    book_id,
                    rating,
                    commentary,
                    created_at,
                    updated_at,
                ) = row

                assert user_id is not None
                assert book_id is not None

                review = Review(
                    user_id=user_id,
                    book_id=book_id,
                    rating=rating,
                    commentary=commentary,
                    created_at=created_at,
                    updated_at=updated_at,
                )

                reviews.append(review)

            return reviews

    def create_or_update_review(
        self,
        *,
        user_id: int,
        book_id: str,
        rating: int,
        commentary: Optional[str] = None,
    ) -> None:
        params = {"user_id": user_id, "book_id": book_id, "rating": rating}

        if commentary is not None:
            params["commentary"] = commentary

        columns = params.keys()

        query = f"""
        INSERT INTO {self._table} ({', '.join(columns)})
        VALUES ({', '.join(map(lambda c: ":" + c, columns))})
        ON CONFLICT (user_id, book_id) DO UPDATE SET
            rating = excluded.rating,
            commentary = excluded.commentary,
            updated_at = CURRENT_TIMESTAMP
        """

        with self._connection_supplier() as connection:
            connection.execute(query, params)
            connection.commit()

    def delete_review(self, *, user_id: int, book_id: str) -> None:
        with self._connection_supplier() as connection:
            connection.execute(
                f"DELETE FROM {self._table} WHERE user_id = ? AND book_id = ?",
                (user_id, book_id),
            )
            connection.commit()
