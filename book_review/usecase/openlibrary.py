from typing import Sequence

import book_review.models.book as models
import book_review.openlibrary.client as openlibrary


class UseCase:
    client: openlibrary.Client

    def __init__(self, client: openlibrary.Client) -> None:
        self.client = client

    async def search_books_previews(self, query: str) -> Sequence[models.BookPreview]:
        books = await self.client.search_books(
            openlibrary.SearchBooksFilter(query=query)
        )

        return list(map(lambda b: b.map(), books))
