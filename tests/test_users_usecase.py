import sqlite3
from typing import Optional

import book_review.db.users as db
import book_review.usecase.users as usecase


def test_verify_password() -> None:
    class MockRepo(db.Repository):
        def find_user_by_id(self, id: int) -> Optional[db.User]:
            raise Exception()

        def find_user_by_login(self, login: str) -> Optional[db.User]:
            raise Exception()

        def create_user(self, login: str, password_hash: str) -> int:
            raise Exception()

        def close(self) -> None:
            raise Exception()

    uc = usecase.UseCase(MockRepo())

    password = "nisi-illo-asperiores"
    hash = uc._hash_password(password)

    assert uc.verify_password(hash, password)
    assert not uc.verify_password(hash, hash)
    assert not uc.verify_password(hash, "delectus-architecto-minima")
    assert not uc.verify_password(
        "$argon2id$v=19$m=65536,t=3,p=4$MIIRqgvgQbgj220jfp0MPA$YfwJSVjtjSU0zzV/P3S9nnQ/USre2wvJMjfCIjrTQbg",
        password,
    )


def test_create_user() -> None:
    expected_login = "login"
    expected_id = 42

    class MockRepo(db.Repository):
        def find_user_by_id(self, id: int) -> Optional[db.User]:
            raise Exception()

        def find_user_by_login(self, login: str) -> Optional[db.User]:
            raise Exception()

        def create_user(self, login: str, password_hash: str) -> int:
            assert login == expected_login

            return expected_id

        def close(self) -> None:
            raise Exception()

    uc = usecase.UseCase(MockRepo())

    id = uc.create_user(expected_login, "ut-nostrum-doloremque")

    assert id == expected_id


def test_find_user_by_id() -> None:
    expected_id = 42
    expected_user = db.User(
        id=expected_id,
        login="login",
        password_hash="hash",
        created_at=sqlite3.Timestamp(1999, 4, 1),
    )

    class MockRepo(db.Repository):
        def find_user_by_id(self, id: int) -> Optional[db.User]:
            assert id == expected_id

            return expected_user

        def find_user_by_login(self, login: str) -> Optional[db.User]:
            raise Exception()

        def create_user(self, login: str, password_hash: str) -> int:
            raise Exception()

        def close(self) -> None:
            raise Exception()

    uc = usecase.UseCase(MockRepo())

    user = uc.find_user_by_id(expected_id)

    assert uc is not None
    assert user == expected_user.map()


def test_find_user_by_login() -> None:
    expected_login = "login"
    expected_user = db.User(
        id=42,
        login=expected_login,
        password_hash="hash",
        created_at=sqlite3.Timestamp(1999, 4, 1),
    )

    class MockRepo(db.Repository):
        def find_user_by_id(self, id: int) -> Optional[db.User]:
            raise Exception()

        def find_user_by_login(self, login: str) -> Optional[db.User]:
            assert login == expected_login

            return expected_user

        def create_user(self, login: str, password_hash: str) -> int:
            raise Exception()

        def close(self) -> None:
            raise Exception()

    uc = usecase.UseCase(MockRepo())

    user = uc.find_user_by_login(expected_login)

    assert uc is not None
    assert user == expected_user.map()
