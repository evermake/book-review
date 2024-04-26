from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import Optional

import pytest
import pytest_asyncio
from pytest_subtests import SubTests
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import book_review.dao.reviews as dao_reviews
import book_review.dao.users as dao_users
from book_review.db import create_all

engine = create_async_engine("sqlite+aiosqlite://")


@pytest_asyncio.fixture
async def session_maker() -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    # can't use :memory: due to yoyo not supporting it

    await create_all(engine)

    session_maker = async_sessionmaker(engine)

    yield session_maker


@pytest_asyncio.fixture
async def users_repo(
    session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[dao_users.Repository, None]:
    yield dao_users.ORMRepository(session_maker)


@pytest_asyncio.fixture
async def reviews_repo(
    session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[dao_reviews.Repository, None]:
    yield dao_reviews.ORMRepository(session_maker)


@pytest.mark.asyncio
async def test_users_create_and_find(
    users_repo: dao_users.Repository, subtests: SubTests
) -> None:
    logins = [f"login{i}" for i in range(10)]

    ids: dict[int, str] = {}
    for login in logins:
        id = await users_repo.create_user(login, "hash")
        ids[id] = login

    for id, login in ids.items():

        def check_user(user: Optional[dao_users.User]) -> None:
            assert user is not None
            assert user.id == id
            assert user.login == login

        with subtests.test("find by id", id=id):
            user = await users_repo.find_user_by_id(id)
            check_user(user)

        with subtests.test("find by login", login=login):
            user = await users_repo.find_user_by_login(login)
            check_user(user)


@pytest.mark.asyncio
async def test_users_not_found(users_repo: dao_users.Repository) -> None:
    user = await users_repo.find_user_by_id(42)
    assert user is None


@pytest.mark.asyncio
async def test_reviews_create_and_find(
    users_repo: dao_users.Repository,
    reviews_repo: dao_reviews.Repository,
    subtests: SubTests,
) -> None:
    user_1 = await users_repo.create_user("Celine_Ratke41", "/1D^C(NHXO")
    user_2 = await users_repo.create_user("Brain_Littel27", "zR|u`VCy]6")

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
        await reviews_repo.create_or_update_review(
            user_id=p.user_id,
            book_id=p.book_id,
            rating=p.rating,
            commentary=p.commentary,
        )

    with subtests.test("find all reviews"):
        reviews = await reviews_repo.find_reviews()

        print(reviews)

        expected_pairs = map(lambda p: (p.user_id, p.book_id), mock_reviews)
        actual_pairs = map(lambda r: (r.user_id, r.book_id), reviews)

        assert all(p in actual_pairs for p in expected_pairs)

    for user_id in [user_1, user_2]:
        with subtests.test("find by user id", user_id=user_id):
            reviews = await reviews_repo.find_reviews(user_id=user_id)

            expected_pairs = map(
                lambda p: (p.user_id, p.book_id),
                filter(lambda p: p.user_id == user_id, mock_reviews),
            )

            actual_pairs = map(lambda r: (r.user_id, r.book_id), reviews)

            assert all(p in actual_pairs for p in expected_pairs)

    for book_id in map(lambda r: r.book_id, mock_reviews):
        with subtests.test("find by book_id", book_id=book_id):
            reviews = await reviews_repo.find_reviews(book_id=book_id)

            expected_pairs = map(
                lambda p: (p.user_id, p.book_id),
                filter(lambda p: p.book_id == book_id, mock_reviews),
            )

            actual_pairs = map(lambda r: (r.user_id, r.book_id), reviews)

            assert all(p in actual_pairs for p in expected_pairs)


@pytest.mark.asyncio
async def test_reviews_not_found(reviews_repo: dao_reviews.Repository) -> None:
    reviews = await reviews_repo.find_reviews(
        book_id="d6c95b45-921b-4aa0-aad2-ea267bfdd036"
    )

    assert len(reviews) == 0
