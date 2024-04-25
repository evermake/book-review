from typing import Optional, Sequence

import book_review.models.book as models
import book_review.openlibrary.client as openlibrary

CoverSize = openlibrary.CoverSize


class UseCase:
    _client: openlibrary.Client

    def __init__(self, client: openlibrary.Client) -> None:
        self._client = client

    async def search_books_previews(self, query: str) -> Sequence[models.BookPreview]:
        books = await self._client.search_books(
            openlibrary.SearchBooksFilter(query=query)
        )

        return list(map(lambda b: b.map(), books))

    async def get_book(self, id: models.BookID) -> Optional[models.Book]:
        book = await self._client.get_book(id)

        if book is None:
            return None

        return book.map()

    async def get_cover(
        self, id: int, size: CoverSize = CoverSize.SMALL
    ) -> Optional[bytes]:
        return await self._client.get_cover(id, size)
