from typing import Optional, Sequence

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from book_review.dao.users import Repository
from book_review.models.user import User, UserID


class UseCase:
    """
    User use cases such authentication, search, creating new users, etc.
    """

    _hasher: PasswordHasher
    _repo: Repository

    def __init__(self, repo: Repository) -> None:
        self._hasher = PasswordHasher()
        self._repo = repo

    async def find_users(self, *, login: Optional[str] = None) -> Sequence[User]:
        """
        Find users by the login substring.
        If the login is not provided it will return all users.
        """

        users = await self._repo.find_users(login_like=login)

        return list(map(lambda u: u.map(), users))

    async def find_user_by_id(self, id: UserID) -> Optional[User]:
        """
        Find a single user by its id.
        If the the user with such id was not found None is returned.
        """

        user = await self._repo.find_user_by_id(id)

        if user is None:
            return None

        return user.map()

    async def find_user_by_login(self, login: str) -> Optional[User]:
        """
        Find a single user by its login.
        If the the user with such login was not found None is returned.
        """

        user = await self._repo.find_user_by_login(login)

        if user is None:
            return None

        return user.map()

    async def create_user(self, login: str, password: str) -> UserID:
        """
        Create a new user.
        Note, that exception will be thrown if the user exists already.
        """

        return await self._repo.create_user(login, self._hash_password(password))

    async def authenticate_user(self, login: str, password: str) -> Optional[User]:
        """
        Retrieve a user by its login and password.
        It will return None if the user was not found or the password is invalid.
        For security, these errors are made indistinguishable on purpose.
        """

        user = await self._repo.find_user_by_login(login)

        if user is None:
            return None

        if not self._verify_password(user.password_hash, password):
            return None

        return user.map()

    def _verify_password(self, hash: str, password: str) -> bool:
        """
        Verify that password and hash matches
        """

        try:
            return self._hasher.verify(hash, password)
        except VerifyMismatchError:
            return False

    def _hash_password(self, password: str) -> str:
        return self._hasher.hash(password)
