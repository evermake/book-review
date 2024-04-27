from unittest.mock import AsyncMock

import pytest

from book_review.models.book import Book, BookID, BookPreview
from book_review.openlibrary.client import Client, CoverSize
from book_review.usecase.openlibrary import UseCase  # Import your UseCase class


@pytest.fixture
def mock_client() -> AsyncMock:
    return AsyncMock(spec=Client)


@pytest.fixture
def use_case(mock_client: AsyncMock) -> UseCase:
    return UseCase(mock_client)


@pytest.mark.asyncio
async def test_search_books_previews(use_case: UseCase, mock_client: AsyncMock) -> None:
    # Arrange
    mock_client.search_books.return_value = [
        AsyncMock(map=lambda: BookPreview(id="123", title="Title1")),
        AsyncMock(map=lambda: BookPreview(id="234", title="Title2")),
    ]
    query = "Harry Potter"

    # Act
    result = await use_case.search_books_previews(query)

    # Assert
    assert len(result) == 2
    assert result[0].title == "Title1"
    assert result[0].id == "123"
    assert result[1].title == "Title2"
    assert result[1].id == "234"


@pytest.mark.asyncio
async def test_get_book(use_case: UseCase, mock_client: AsyncMock) -> None:
    # Arrange
    mock_client.get_book.return_value = AsyncMock(
        map=lambda: Book(id="123", title="Title", description="Description")
    )

    # Act
    result = await use_case.get_book(BookID("123"))

    if result is not None:
        assert result.title == "Title"
        assert result.description == "Description"

    # Assert
    assert result is not None


@pytest.mark.asyncio
async def test_get_book_not_found(use_case: UseCase, mock_client: AsyncMock) -> None:
    # Arrange
    mock_client.get_book.return_value = None

    # Act
    result = await use_case.get_book(BookID("123"))

    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_get_cover(use_case: UseCase, mock_client: AsyncMock) -> None:
    # Arrange
    mock_client.get_cover.return_value = b"fake_cover_data"
    book_id = 123
    expected_size = CoverSize.SMALL

    # Act
    result = await use_case.get_cover(book_id, expected_size)

    # Assert
    assert result == b"fake_cover_data"


@pytest.mark.asyncio
async def test_get_cover_not_found(use_case: UseCase, mock_client: AsyncMock) -> None:
    # Arrange
    mock_client.get_cover.return_value = None
    book_id = 123
    expected_size = CoverSize.SMALL

    # Act
    result = await use_case.get_cover(book_id, expected_size)

    # Assert
    assert result is None
