from typing import AsyncGenerator

import pytest
import pytest_asyncio
from aiohttp import ClientSession

from book_review.config import settings
from book_review.openlibrary.client import Client, HTTPAPIClient, SearchBooksFilter


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[Client, None]:
    yield HTTPAPIClient(
        api_session=ClientSession(settings.OPENLIBRARY_BASE_URL),
        covers_session=ClientSession(settings.OPENLIBRARY_COVERS_BASE_URL),
    )


@pytest.mark.asyncio
async def test_search_books(client: Client) -> None:
    books = await client.search_books(SearchBooksFilter(query="lord of rings"))

    assert len(books)
