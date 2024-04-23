from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Sequence

import aiohttp
from pydantic import BaseModel, PositiveInt
from yarl import URL

import book_review.models.book as models

BASE_URL = URL("https://openlibrary.org/")

QueryParams = list[tuple[str, str]]


class Sort(str, Enum):
    EditionsCountDesc = "editions"

    Old = "old"
    New = "new"

    RatingAsc = "rating asc"
    RatingDesc = "rating desc"

    TitleAsc = "title"

    RandomAsc = "random asc"
    RandomDesc = "random desc"
    RandomHourly = "random.hourly"
    RandomDaily = "random.daily"

    KeyAsc = "key asc"
    KeyDesc = "key desc"


class SearchBooksFilter(BaseModel):
    query: Optional[str] = None
    sort: Optional[Sort] = None
    language: Optional[str] = None
    page: Optional[PositiveInt] = None
    limit: Optional[PositiveInt] = None


class Book(BaseModel):
    key: str
    title: str
    author_key: Sequence[str] = []
    author_name: Sequence[str] = []
    language: Sequence[str] = []
    publish_year: Sequence[int] = []
    subject: Sequence[str] = []

    def map(self) -> models.Book:
        raise NotImplementedError()


class Client(ABC):
    """
    Client for the OpenLibrary.

    See: https://openlibrary.org/developers/api
    """

    @abstractmethod
    async def search_books(self, filter: SearchBooksFilter) -> Sequence[Book]:
        pass


class HTTPAPIClient(Client):
    _http_client: aiohttp.ClientSession

    def __init__(self, base_url: URL = BASE_URL) -> None:
        super().__init__()

        self._http_client = aiohttp.ClientSession(base_url)

    @staticmethod
    def _build_search_books_filters_params(filter: SearchBooksFilter) -> QueryParams:
        params: QueryParams = []

        if filter.query is not None:
            params.append(("q", filter.query))

        if filter.sort is not None:
            params.append(("sort", filter.sort))

        if filter.language is not None:
            params.append(("lang", filter.language))

        if filter.page is not None:
            params.append(("page", str(filter.page)))

        if filter.limit is not None:
            params.append(("limit", str(filter.limit)))

        # add only required fields so that response is smaller and faster
        params.append(("fields", ",".join(Book.model_fields.keys())))

        return params

    async def search_books(self, filter: SearchBooksFilter) -> Sequence[Book]:
        params = self._build_search_books_filters_params(filter)

        async with self._http_client.get("/search.json", params=params) as resp:
            if resp.status != 200:
                raise Exception(f"unexpected status {resp.status}")

            class Response(BaseModel):
                docs: Sequence[Book]

            return Response(**await resp.json()).docs
