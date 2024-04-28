from abc import ABC, abstractmethod
from datetime import date
from enum import Enum
from typing import Optional, Sequence

import aiohttp
from pydantic import BaseModel, PositiveInt

import book_review.models.book as models

QueryParams = list[tuple[str, str]]


class CoverSize(str, Enum):
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"


class Sort(str, Enum):
    EDITIONS_COUNT_DESC = "editions"

    OLD = "old"
    NEW = "new"

    RATING_ASC = "rating asc"
    RATING_DESC = "rating desc"

    TITLE_ASC = "title"

    RANDOM_ASC = "random asc"
    RANDOM_DESC = "random desc"
    RANDOM_HOURLY = "random.hourly"
    RANDOM_DAILY = "random.daily"

    KEY_ASC = "key asc"
    KEY_DESC = "key desc"


class SearchBooksFilter(BaseModel):
    query: Optional[str] = None
    sort: Optional[Sort] = None
    language: Optional[str] = None
    page: Optional[PositiveInt] = None
    limit: Optional[PositiveInt] = None


class BookPreview(BaseModel):
    key: str
    title: str
    cover_i: Optional[int] = None
    author_key: Sequence[str] = []
    author_name: Sequence[str] = []
    language: Sequence[str] = []
    publish_year: Sequence[int] = []
    subject: Sequence[str] = []

    def map(self) -> models.BookPreview:
        authors = [
            models.Author(id=key, name=name)
            for key, name in zip(self.author_key, self.author_name)
        ]

        first_year: Optional[int] = None

        for year in self.publish_year:
            if year <= 0:
                continue

            if first_year is not None:
                first_year = min(first_year or 1, year)
            else:
                first_year = year

        first_publishment_date: Optional[date] = None

        if first_year is not None:
            first_publishment_date = date(year=first_year, month=1, day=1)

        return models.BookPreview(
            id=self.key,
            title=self.title,
            cover_id=self.cover_i,
            authors=authors,
            first_publishment_date=first_publishment_date,
            subjects=self.subject,
            languages=self.language,
        )


class Book(BaseModel):
    key: str
    title: str
    description: Optional[str] = None
    covers: Sequence[int] = []
    subjects: Sequence[str] = []

    def map(self) -> models.Book:
        return models.Book(
            id=self.key,
            title=self.title,
            description=self.description,
            covers=self.covers,
            subjects=self.subjects,
        )


def adjust_key(key: str) -> str:
    """
    Adjust openlibrary key from "/works/OL49024" to "OL49024"
    """

    return key.split("/")[-1]


def normalize_query(query: str) -> str:
    """
    Normalize given query by removing odd spaces and making it lowercase.
    It is used for a better caching
    """

    # ignore case
    query = query.lower()

    # remove trailing spaces, replace multiple spaces with one
    query = " ".join(query.split())

    return query


class Client(ABC):
    """
    Client for the OpenLibrary.

    See: https://openlibrary.org/developers/api
    """

    @abstractmethod
    async def search_books(self, filter: SearchBooksFilter) -> Sequence[BookPreview]:
        """
        Search books previews with the given filter.
        Book preview does not hold all available information for the sake of performance.
        Use `get_book` to get more information for a specific book.
        """
        pass

    @abstractmethod
    async def get_book(self, key: str) -> Optional[Book]:
        """
        Get specific book by the given key.
        It will return None if the book was not found.
        """
        pass

    @abstractmethod
    async def get_cover(
        self, id: int, size: CoverSize = CoverSize.SMALL
    ) -> Optional[bytes]:
        """
        Get book or author cover image bytes by its id.
        It will return None if the cover was not found.
        """
        pass


class HTTPAPIClient(Client):
    """
    Openlibrary client based on their HTTP API
    """

    _api: aiohttp.ClientSession
    _covers: aiohttp.ClientSession

    def __init__(
        self,
        *,
        api_session: aiohttp.ClientSession,
        covers_session: aiohttp.ClientSession,
    ) -> None:
        super().__init__()

        self._api = api_session
        self._covers = covers_session

    @staticmethod
    def _build_search_books_filters_params(filter: SearchBooksFilter) -> QueryParams:
        """
        Build API query parameters from the given filter.
        """

        params: QueryParams = []

        if filter.query is not None:
            params.append(("q", normalize_query(filter.query)))

        if filter.sort is not None:
            params.append(("sort", filter.sort))

        if filter.language is not None:
            params.append(("lang", filter.language))

        if filter.page is not None:
            params.append(("page", str(filter.page)))

        if filter.limit is not None:
            params.append(("limit", str(filter.limit)))

        # add only required fields so that response is smaller and faster
        params.append(("fields", ",".join(BookPreview.model_fields.keys())))

        return params

    async def search_books(self, filter: SearchBooksFilter) -> Sequence[BookPreview]:
        params = self._build_search_books_filters_params(filter)

        async with self._api.get("/search.json", params=params) as resp:
            if resp.status != 200:
                raise Exception(f"unexpected status {resp.status}")

            class Response(BaseModel):
                docs: Sequence[BookPreview]

            books = Response(**await resp.json()).docs

            for book in books:
                book.key = adjust_key(book.key)

            return books

    async def get_book(self, key: str) -> Optional[Book]:
        async with self._api.get(f"/works/{key}.json") as resp:
            if resp.status == 404:
                return None

            if resp.status != 200:
                raise Exception(f"unexpected status {resp.status}")

            book = Book(**await resp.json())

            book.key = adjust_key(book.key)

            return book

    async def get_cover(
        self, id: int, size: CoverSize = CoverSize.SMALL
    ) -> Optional[bytes]:
        async with self._covers.get(f"/b/id/{id}-{size.value}.jpg") as resp:
            if resp.status == 404:
                return None

            if resp.status != 200:
                raise Exception(f"unexpected status {resp.status}")

            # TODO: stream the response instead to avoid loading entire image into RAM
            return await resp.content.read()
