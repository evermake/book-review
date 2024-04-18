from typing import Optional
from pydantic import BaseModel, PositiveInt

from book_review.models.book import BookPreview, Book, BookID

from abc import ABC, abstractmethod


class SearchBooksFilter(BaseModel):
    query: Optional[str]
    sort: Optional[str]
    language: Optional[str]
    page: Optional[PositiveInt]
    limit: Optional[PositiveInt]


class LibraryClient(ABC):
    @abstractmethod
    async def search_books_previews(
        self, filter: SearchBooksFilter
    ) -> list[BookPreview]:
        pass

    @abstractmethod
    async def get_book(self, id: BookID) -> Book:
        pass
