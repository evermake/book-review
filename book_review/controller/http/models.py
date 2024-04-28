from datetime import date, datetime
from typing import Optional, Sequence

from pydantic import BaseModel

import book_review.models.book as book_models
import book_review.models.reviews as reviews_models
import book_review.models.user as user_models
import book_review.usecase.openlibrary as openlibrary_usecase

UserID = user_models.UserID
BookID = book_models.BookID
AuthorID = book_models.AuthorID
CoverID = book_models.CoverID

CoverSize = openlibrary_usecase.CoverSize


class User(BaseModel):
    id: UserID
    login: str
    created_at: datetime

    @staticmethod
    def parse(user: user_models.User) -> "User":
        return User(id=user.id, login=user.login, created_at=user.created_at)


class ReviewRequest(BaseModel):
    book_id: BookID
    rating: int
    commentary: Optional[str]


class Review(BaseModel):
    user_id: UserID
    book_id: BookID
    rating: int
    commentary: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    @staticmethod
    def parse(review: reviews_models.Review) -> "Review":
        return Review(
            user_id=review.user_id,
            book_id=review.book_id,
            rating=review.rating,
            commentary=review.commentary,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )


class Author(BaseModel):
    id: AuthorID
    name: str

    @staticmethod
    def parse(author: book_models.Author) -> "Author":
        return Author(id=author.id, name=author.name)


class BookPreview(BaseModel):
    id: BookID
    title: str
    authors: Sequence[Author] = []
    first_publishment_date: Optional[date] = None
    subjects: Sequence[str] = []
    languages: Sequence[str] = []

    @staticmethod
    def parse(book: book_models.BookPreview) -> "BookPreview":
        authors = list(map(lambda a: Author.parse(a), book.authors))

        return BookPreview(
            id=book.id,
            title=book.title,
            authors=authors,
            first_publishment_date=book.first_publishment_date,
            subjects=book.subjects,
            languages=book.languages,
        )


class Book(BaseModel):
    id: BookID
    title: str
    description: Optional[str] = None
    covers: Sequence[int] = []
    subjects: Sequence[str] = []

    @staticmethod
    def parse(book: book_models.Book) -> "Book":
        return Book(
            id=book.id,
            title=book.title,
            description=book.description,
            covers=book.covers,
            subjects=book.subjects,
        )
