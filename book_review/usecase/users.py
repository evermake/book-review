from typing import Optional, Sequence

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from book_review.db.users import Repository
from book_review.models.user import User, UserID


class UseCase:
    _hasher: PasswordHasher
    _repo: Repository

    def __init__(self, repo: Repository) -> None:
        self._hasher = PasswordHasher()
        self._repo = repo

    def find_users(self, *, login: Optional[str] = None) -> Sequence[User]:
        """
        Find users by the login substring.
        If the login is not provided it will return all users.
        """

        users = self._repo.find_users(login_like=login)

        return list(map(lambda u: u.map(), users))

    def find_user_by_id(self, id: UserID) -> Optional[User]:
        user = self._repo.find_user_by_id(id)

        if user is None:
            return None

        return user.map()

    def find_user_by_login(self, login: str) -> Optional[User]:
        user = self._repo.find_user_by_login(login)

        if user is None:
            return None

        return user.map()

    def create_user(self, login: str, password: str) -> UserID:
        # TODO: make usecase own UserExistsError and map it
        return self._repo.create_user(login, self._hash_password(password))

    def authenticate_user(self, login: str, password: str) -> Optional[User]:
        """
        Retrieve a user by its login and password.
        It will return None if the user was not found or the password is invalid.
        For security, these errors are made indistinguishable on purpose.
        """

        user = self._repo.find_user_by_login(login)

        if user is None:
            return None

        if not self._verify_password(user.password_hash, password):
            return None

        return user.map()

    def _verify_password(self, hash: str, password: str) -> bool:
        try:
            return self._hasher.verify(hash, password)
        except VerifyMismatchError:
            return False

    def _hash_password(self, password: str) -> str:
        return self._hasher.hash(password)
