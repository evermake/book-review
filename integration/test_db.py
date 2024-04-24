import os
import sqlite3
import uuid
from dataclasses import dataclass
from typing import Generator, Optional

import pytest
from pytest_subtests import SubTests

import book_review.db.reviews as db_reviews
import book_review.db.users as db
from book_review.db.repository import ConnectionSupplier, apply_migrations


@pytest.fixture
def connection_supplier() -> Generator[ConnectionSupplier, None, None]:
    # can't use :memory: due to yoyo not supporting it
    DB = f"db.test.{uuid.uuid4()}.sqlite3"

    apply_migrations(f"sqlite:///{DB}")

    yield lambda: sqlite3.connect(DB)

    os.remove(DB)


@pytest.fixture
def users_repo(
    connection_supplier: ConnectionSupplier,
) -> Generator[db.Repository, None, None]:
    yield db.SQLiteRepository(connection_supplier)


@pytest.fixture
def reviews_repo(
    connection_supplier: ConnectionSupplier,
) -> Generator[db_reviews.Repository, None, None]:
    yield db_reviews.SQLiteRepository(connection_supplier)


def test_users_create_and_find(users_repo: db.Repository, subtests: SubTests) -> None:
    logins = [f"login{i}" for i in range(10)]

    ids: dict[int, str] = {}
    for login in logins:
        id = users_repo.create_user(login, "hash")
        ids[id] = login

    for id, login in ids.items():

        def check_user(user: Optional[db.User]) -> None:
            assert user is not None
            assert user.id == id
            assert user.login == login

        with subtests.test("find by id", id=id):
            user = users_repo.find_user_by_id(id)
            check_user(user)

        with subtests.test("find by login", login=login):
            user = users_repo.find_user_by_login(login)
            check_user(user)


def test_users_not_found(users_repo: db.Repository) -> None:
    user = users_repo.find_user_by_id(42)
    assert user is None


def test_reviews_create_and_find(
    users_repo: db.Repository,
    reviews_repo: db_reviews.Repository,
    subtests: SubTests,
) -> None:
    user_1 = users_repo.create_user("Celine_Ratke41", "/1D^C(NHXO")
    user_2 = users_repo.create_user("Brain_Littel27", "zR|u`VCy]6")

    @dataclass
    class MockReview:
        user_id: int
        book_id: str
        rating: int
        commentary: Optional[str] = None

    mock_reviews: list[MockReview] = [
        MockReview(
            user_1,
            "110bc36b-67d6-4130-b1a9-3da953691c17",
            8,
            "Consequatur incidunt reiciendis ea ex aut doloremque commodi.",
        ),
        MockReview(
            user_1,
            "fda52a24-baae-4580-b3b9-343f8d8d4b07",
            10,
            None,
        ),
        MockReview(
            user_2,
            "4f05cbd3-3d61-4f5c-a8b1-c23bd8317ea5",
            1,
            None,
        ),
    ]

    for p in mock_reviews:
        reviews_repo.create_or_update_review(
            p.user_id, p.book_id, p.rating, p.commentary
        )

    with subtests.test("find all reviews"):
        reviews = reviews_repo.find_reviews()

        expected_pairs = map(lambda p: (p.user_id, p.book_id), mock_reviews)
        actual_pairs = map(lambda r: (r.user_id, r.book_id), reviews)

        assert all(p in actual_pairs for p in expected_pairs)

    for user_id in [user_1, user_2]:
        with subtests.test("find by user id", user_id=user_id):
            reviews = reviews_repo.find_reviews(user_id=user_id)

            expected_pairs = map(
                lambda p: (p.user_id, p.book_id),
                filter(lambda p: p.user_id == user_id, mock_reviews),
            )

            actual_pairs = map(lambda r: (r.user_id, r.book_id), reviews)

            assert all(p in actual_pairs for p in expected_pairs)

    for book_id in map(lambda r: r.book_id, mock_reviews):
        with subtests.test("find by book_id", book_id=book_id):
            reviews = reviews_repo.find_reviews(book_id=book_id)

            expected_pairs = map(
                lambda p: (p.user_id, p.book_id),
                filter(lambda p: p.book_id == book_id, mock_reviews),
            )

            actual_pairs = map(lambda r: (r.user_id, r.book_id), reviews)

            assert all(p in actual_pairs for p in expected_pairs)


def test_reviews_not_found(reviews_repo: db_reviews.Repository) -> None:
    reviews = reviews_repo.find_reviews(book_id="d6c95b45-921b-4aa0-aad2-ea267bfdd036")

    assert len(reviews) == 0
