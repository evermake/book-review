from book_review.library.client import LibraryClient, SearchBooksFilter
from book_review.models.book import Book, BookPreview

from .book import BookID


class UseCase:
    client: LibraryClient

    def __init__(self, client: LibraryClient) -> None:
        self.client = client

    async def search_books_previews(
        self, filter: SearchBooksFilter
    ) -> list[BookPreview]:
        return await self.client.search_books_previews(filter)

    async def get_book(self, id: BookID) -> Book:
        return await self.client.get_book(id)
