from book_review.models.book import Book, BookID, BookPreview

from .client import LibraryClient, SearchBooksFilter


class OpenLibraryClient(LibraryClient):
    def __init__(self) -> None:
        super().__init__()

    async def search_books_previews(
        self, filter: SearchBooksFilter
    ) -> list[BookPreview]: ...

    async def get_book(self, id: BookID) -> Book: ...
