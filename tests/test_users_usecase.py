import sqlite3
from typing import Optional, Sequence

import pytest

import book_review.db.users as db
import book_review.usecase.users as usecase


@pytest.mark.asyncio
async def test_verify_password() -> None:
    class MockRepo(db.Repository):
        async def find_users(
            self, *, login_like: Optional[str] = None
        ) -> Sequence[db.User]:
            raise Exception()

        async def find_user_by_id(self, id: db.UserID) -> Optional[db.User]:
            raise Exception()

        async def find_user_by_login(self, login: str) -> Optional[db.User]:
            raise Exception()

        async def create_user(self, login: str, password_hash: str) -> int:
            raise Exception()

    uc = usecase.UseCase(MockRepo())

    password = "nisi-illo-asperiores"
    hash = uc._hash_password(password)

    assert uc._verify_password(hash, password)
    assert not uc._verify_password(hash, hash)
    assert not uc._verify_password(hash, "delectus-architecto-minima")
    assert not uc._verify_password(
        "$argon2id$v=19$m=65536,t=3,p=4$MIIRqgvgQbgj220jfp0MPA$YfwJSVjtjSU0zzV/P3S9nnQ/USre2wvJMjfCIjrTQbg",
        password,
    )


@pytest.mark.asyncio
async def test_create_user() -> None:
    expected_login = "login"
    expected_id = 42

    class MockRepo(db.Repository):
        async def find_users(
            self, *, login_like: Optional[str] = None
        ) -> Sequence[db.User]:
            raise Exception()

        async def find_user_by_id(self, id: int) -> Optional[db.User]:
            raise Exception()

        async def find_user_by_login(self, login: str) -> Optional[db.User]:
            raise Exception()

        async def create_user(self, login: str, password_hash: str) -> int:
            assert login == expected_login

            return expected_id

    uc = usecase.UseCase(MockRepo())

    id = await uc.create_user(expected_login, "ut-nostrum-doloremque")

    assert id == expected_id


@pytest.mark.asyncio
async def test_find_user_by_id() -> None:
    expected_id = 42
    expected_user = db.User(
        id=expected_id,
        login="login",
        password_hash="hash",
        created_at=sqlite3.Timestamp(1999, 4, 1),
    )

    class MockRepo(db.Repository):
        async def find_users(
            self, *, login_like: Optional[str] = None
        ) -> Sequence[db.User]:
            raise Exception()

        async def find_user_by_id(self, id: int) -> Optional[db.User]:
            assert id == expected_id

            return expected_user

        async def find_user_by_login(self, login: str) -> Optional[db.User]:
            raise Exception()

        async def create_user(self, login: str, password_hash: str) -> int:
            raise Exception()

    uc = usecase.UseCase(MockRepo())

    user = await uc.find_user_by_id(expected_id)

    assert uc is not None
    assert user == expected_user.map()


@pytest.mark.asyncio
async def test_find_user_by_login() -> None:
    expected_login = "login"
    expected_user = db.User(
        id=42,
        login=expected_login,
        password_hash="hash",
        created_at=sqlite3.Timestamp(1999, 4, 1),
    )

    class MockRepo(db.Repository):
        async def find_users(
            self, *, login_like: Optional[str] = None
        ) -> Sequence[db.User]:
            raise Exception()

        async def find_user_by_id(self, id: int) -> Optional[db.User]:
            raise Exception()

        async def find_user_by_login(self, login: str) -> Optional[db.User]:
            assert login == expected_login

            return expected_user

        async def create_user(self, login: str, password_hash: str) -> int:
            raise Exception()

    uc = usecase.UseCase(MockRepo())

    user = await uc.find_user_by_login(expected_login)

    assert uc is not None
    assert user == expected_user.map()
