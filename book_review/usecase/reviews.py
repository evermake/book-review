from typing import Optional, Sequence

from book_review.db.reviews import Repository
from book_review.models.book import BookID
from book_review.models.reviews import Review
from book_review.models.user import UserID


class UseCase:
    _repo: Repository

    def __init__(self, repo: Repository) -> None:
        self._repo = repo

    def create_or_update_review(
        self,
        user_id: UserID,
        book_id: BookID,
        rating: int,
        commentary: Optional[str] = None,
    ) -> None:
        self._repo.create_or_update_review(user_id, book_id, rating, commentary)

    def find_reviews(
        self, book_id: Optional[BookID] = None, user_id: Optional[UserID] = None
    ) -> Sequence[Review]:
        reviews = self._repo.find_reviews(book_id, user_id)

        return list(map(lambda r: r.map(), reviews))
