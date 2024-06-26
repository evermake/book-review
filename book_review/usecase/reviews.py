from typing import Optional, Sequence

from book_review.dao.reviews import Repository
from book_review.models.book import BookID
from book_review.models.reviews import Review
from book_review.models.user import UserID


class UseCase:
    """
    Book reviews use cases.
    """

    _repo: Repository

    def __init__(self, repo: Repository) -> None:
        self._repo = repo

    async def create_or_update_review(
        self,
        user_id: UserID,
        book_id: BookID,
        rating: int,
        commentary: Optional[str] = None,
    ) -> None:
        """
        Create a new review or update an existing one.
        """

        await self._repo.create_or_update_review(
            user_id=user_id, book_id=book_id, rating=rating, commentary=commentary
        )

    async def find_reviews(
        self, book_id: Optional[BookID] = None, user_id: Optional[UserID] = None
    ) -> Sequence[Review]:
        """
        Find reviews by optionally limiting the results by specific book and/or user.
        """

        reviews = await self._repo.find_reviews(book_id=book_id, user_id=user_id)

        return list(map(lambda r: r.map(), reviews))

    async def delete_review(self, user_id: UserID, book_id: BookID) -> None:
        """
        Delete a review.
        This method is idempotent - calling this method multiple times would not raise an error.
        """

        await self._repo.delete_review(user_id=user_id, book_id=book_id)
