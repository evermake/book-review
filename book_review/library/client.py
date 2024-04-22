from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel, PositiveInt

from book_review.models.book import Book, BookID, BookPreview


class SearchBooksFilter(BaseModel):
    query: Optional[str] = None
    sort: Optional[str] = None
    language: Optional[str] = None
    page: Optional[PositiveInt] = None
    limit: Optional[PositiveInt] = None


class LibraryClient(ABC):
    @abstractmethod
    async def search_books_previews(
        self, filter: SearchBooksFilter
    ) -> list[BookPreview]:
        pass

    @abstractmethod
    async def get_book(self, id: BookID) -> Book:
        pass
