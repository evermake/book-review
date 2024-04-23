from typing import AsyncGenerator

import pytest
import pytest_asyncio

from book_review.openlibrary.client import Client, HTTPAPIClient, SearchBooksFilter


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[Client, None]:
    yield HTTPAPIClient()


@pytest.mark.asyncio
async def test_search_books(client: Client) -> None:
    print(client)
    books = await client.search_books(SearchBooksFilter(query="lord of rings"))
    assert len(books)
