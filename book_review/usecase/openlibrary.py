from typing import Optional, Sequence

import book_review.models.book as models
import book_review.openlibrary.client as openlibrary

CoverSize = openlibrary.CoverSize


class UseCase:
    """
    Openlibrary use cases
    """

    _client: openlibrary.Client

    def __init__(self, client: openlibrary.Client) -> None:
        self._client = client

    async def search_books_previews(self, query: str) -> Sequence[models.BookPreview]:
        """
        Search books previews for the given title query.
        Book preview does not hold all available information for the sake of performance.
        Use `get_book` to get more information for a specific book.
        """

        books = await self._client.search_books(
            openlibrary.SearchBooksFilter(query=query)
        )

        return list(map(lambda b: b.map(), books))

    async def get_book(self, id: models.BookID) -> Optional[models.Book]:
        """
        Get all available book information by its id.
        If the book with such id was not found None is returned.
        """

        book = await self._client.get_book(id)

        if book is None:
            return None

        return book.map()

    async def get_cover(
        self, id: int, size: CoverSize = CoverSize.SMALL
    ) -> Optional[bytes]:
        """
        Get book or author cover image by its id as bytes.
        If the image with such id was not found None is returned.
        """

        # TODO: stream the image instead
        return await self._client.get_cover(id, size)

    async def get_author(self, id: models.AuthorID) -> Optional[models.Author]:
        author = await self._client.get_author(id)

        if author is None:
            return None

        return author.map()
