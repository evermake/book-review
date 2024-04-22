from typing import Optional

import book_review.db.users as db
import book_review.usecase.users as usecase


def test_verify_password() -> None:
    class MockRepo(db.Repository):
        def find_user_by_id(self, id: int) -> Optional[db.User]:
            return None

        def find_user_by_login(self, login: str) -> Optional[db.User]:
            return None

        def create_user(self, login: str, password_hash: str) -> int:
            return 0

        def close(self) -> None:
            pass

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
