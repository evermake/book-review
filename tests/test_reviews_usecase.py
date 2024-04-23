import random
import sqlite3
from typing import Optional, Sequence

import book_review.db.reviews as db
import book_review.usecase.reviews as usecase


def test_create_review() -> None:
    expected_user_id = 42
    expected_book_id = "272c8d0f-6e95-4089-a3b1-6e51a2e3261c"
    expected_rating = 8
    expected_commentary = "Laboriosam reprehenderit dolores porro vitae."

    class MockRepo(db.Repository):
        def create_review(
            self,
            user_id: int,
            book_id: str,
            rating: int,
            commentary: Optional[str] = None,
        ) -> None:
            assert user_id == expected_user_id
            assert book_id == expected_book_id
            assert rating == expected_rating
            assert commentary == expected_commentary

        def find_reviews(
            self, book_id: Optional[str] = None, user_id: Optional[int] = None
        ) -> Sequence[db.Review]:
            raise Exception()

        def close(self) -> None:
            raise Exception()

    uc = usecase.UseCase(MockRepo())

    uc.create_review(
        expected_user_id, expected_book_id, expected_rating, expected_commentary
    )


def test_find_reviews() -> None:
    expected_book_id = "d8feda9d-82f6-4f05-821c-70daa6b627af"
    expected_user_id = 42

    expected_reviews: list[db.Review] = []

    for i in range(10):
        review = db.Review(
            user_id=expected_user_id,
            book_id=expected_book_id,
            rating=random.randint(1, 10),
            created_at=sqlite3.Timestamp(2024, 1, 1),
        )

        expected_reviews.append(review)

    class MockRepo(db.Repository):
        def create_review(
            self,
            user_id: int,
            book_id: str,
            rating: int,
            commentary: Optional[str] = None,
        ) -> None:
            raise Exception()

        def find_reviews(
            self, book_id: Optional[str] = None, user_id: Optional[int] = None
        ) -> Sequence[db.Review]:
            assert book_id == expected_book_id
            assert user_id == expected_user_id

            return expected_reviews

        def close(self) -> None:
            raise Exception()

    uc = usecase.UseCase(MockRepo())

    reviews = uc.find_reviews(expected_book_id, expected_user_id)

    for actual, expected in zip(reviews, expected_reviews):
        assert actual.user_id == expected.user_id
        assert actual.book_id == expected.book_id
        assert actual.rating == expected.rating
        assert actual.commentary == expected.commentary
        assert actual.created_at == expected.created_at
        assert actual.updated_at == expected.updated_at
