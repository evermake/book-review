import random
import sqlite3
from typing import Optional, Sequence

import pytest

import book_review.dao.reviews as dao
import book_review.usecase.reviews as usecase


@pytest.mark.asyncio
async def test_create_review() -> None:
    expected_user_id = 42
    expected_book_id = "272c8d0f-6e95-4089-a3b1-6e51a2e3261c"
    expected_rating = 8
    expected_commentary = "Laboriosam reprehenderit dolores porro vitae."

    class MockRepo(dao.Repository):
        async def delete_review(self, *, user_id: int, book_id: str) -> None:
            raise Exception()

        async def create_or_update_review(
            self,
            *,
            user_id: int,
            book_id: str,
            rating: int,
            commentary: Optional[str] = None,
        ) -> None:
            assert user_id == expected_user_id
            assert book_id == expected_book_id
            assert rating == expected_rating
            assert commentary == expected_commentary

        async def find_reviews(
            self, *, book_id: Optional[str] = None, user_id: Optional[int] = None
        ) -> Sequence[dao.Review]:
            raise Exception()

        async def close(self) -> None:
            raise Exception()

    uc = usecase.UseCase(MockRepo())

    await uc.create_or_update_review(
        expected_user_id, expected_book_id, expected_rating, expected_commentary
    )


@pytest.mark.asyncio
async def test_find_reviews() -> None:
    expected_book_id = "d8feda9d-82f6-4f05-821c-70daa6b627af"
    expected_user_id = 42

    expected_reviews: list[dao.Review] = []

    for _ in range(10):
        review = dao.Review(
            user_id=expected_user_id,
            book_id=expected_book_id,
            rating=random.randint(1, 10),
            created_at=sqlite3.Timestamp(2024, 1, 1),
        )

        expected_reviews.append(review)

    class MockRepo(dao.Repository):
        async def delete_review(self, *, user_id: int, book_id: str) -> None:
            raise Exception()

        async def create_or_update_review(
            self,
            *,
            user_id: int,
            book_id: str,
            rating: int,
            commentary: Optional[str] = None,
        ) -> None:
            raise Exception()

        async def find_reviews(
            self, *, book_id: Optional[str] = None, user_id: Optional[int] = None
        ) -> Sequence[dao.Review]:
            assert book_id == expected_book_id
            assert user_id == expected_user_id

            return expected_reviews

    uc = usecase.UseCase(MockRepo())

    reviews = await uc.find_reviews(expected_book_id, expected_user_id)

    for actual, expected in zip(reviews, expected_reviews):
        assert actual.user_id == expected.user_id
        assert actual.book_id == expected.book_id
        assert actual.rating == expected.rating
        assert actual.commentary == expected.commentary
        assert actual.created_at == expected.created_at
        assert actual.updated_at == expected.updated_at
