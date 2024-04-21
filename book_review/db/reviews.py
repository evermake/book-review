import sqlite3
from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

import book_review.db.repository as db


class Review(BaseModel):
    user_id: int
    book_id: str
    rating: int
    commentary: str
    created_at: sqlite3.Timestamp
    updated_at: Optional[sqlite3.Timestamp]


class Repository(db.Repository):
    @abstractmethod
    def create_review(
        self, user_id: int, book_id: str, rating: int, commentary: Optional[str] = None
    ) -> Optional[int]:
        pass

    @abstractmethod
    def find_reviews(
        self, book_id: Optional[str], user_id: Optional[int]
    ) -> list[Review]:
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

    def find_reviews(
        self, book_id: Optional[str], user_id: Optional[int]
    ) -> list[Review]:
        query = "SELECT user_id, book_id, rating, commentary, created_at, updated_at, edited_at FROM reviews"

        params: dict[str, str | int] = dict()

        if book_id is not None:
            params["book_id"] = book_id

        if user_id is not None:
            params["user_id"] = user_id

        if params:
            statements = []

            if params["book_id"]:
                statements.append("book_id = :book_id")

            if params["user_id"]:
                statements.append("user_id = :user_id")

            query += f" WHERE {' AND '.join(statements)}"

        cursor = self.connection.cursor()
        cursor.execute(query, params)

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

    def create_review(
        self, user_id: int, book_id: str, rating: int, commentary: Optional[str] = None
    ) -> Optional[int]:
        params = {"user_id": user_id, "book_id": book_id, "rating": rating}

        if commentary is not None:
            params["commentary"] = commentary

        columns = map(lambda c: c[0], params)

        query = f"""
        INSERT INTO reviews ({', '.join(columns)})
        VALUES ({', '.join(map(lambda c: ":" + c, columns))})
        RETURNING id
        """

        cursor = self.connection.cursor()
        cursor.execute(query, params)

        self.connection.commit()

        row = cursor.fetchone()

        if row is None:
            return None

        (id,) = row

        return int(id)
