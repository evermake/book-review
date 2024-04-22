from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from book_review.db.users import Repository
from book_review.models.user import User, UserID


class UseCase:
    _hasher: PasswordHasher

    repo: Repository

    def __init__(self, repo: Repository) -> None:
        self._hasher = PasswordHasher()
        self.repo = repo

    def find_user(self, id: UserID) -> Optional[User]:
        user = self.repo.find_user_by_id(id)

        if user is None:
            return None

        return user.map()

    def create_user(self, login: str, password: str) -> UserID:
        return self.repo.create_user(login, self._hash_password(password))

    def verify_password(self, hash: str, password: str) -> bool:
        try:
            return self._hasher.verify(hash, password)
        except VerifyMismatchError:
            return False

    def _hash_password(self, password: str) -> str:
        return self._hasher.hash(password)
