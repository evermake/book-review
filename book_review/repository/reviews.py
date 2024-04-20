import book_review.repository.repository as repository
import sqlite3
from typing import Optional
from pydantic import BaseModel


class Review(BaseModel):
    user_id: int
    book_id: int
    rating: int
    commentary: str
    created_at: sqlite3.Timestamp
    edited_at: Optional[sqlite3.Timestamp]


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

        row = cursor.fetchone()

        if row is None:
            return None

        (id,) = row

        return int(id)
