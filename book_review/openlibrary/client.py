from abc import ABC, abstractmethod
from typing import Optional, Sequence

import aiohttp
from pydantic import BaseModel, PositiveInt
from yarl import URL

import book_review.models.book as models

BASE_URL = URL("https://openlibrary.org/")

QueryParams = list[tuple[str, str]]


class SearchBooksFilter(BaseModel):
    query: Optional[str] = None
    sort: Optional[str] = None
    language: Optional[str] = None
    page: Optional[PositiveInt] = None
    limit: Optional[PositiveInt] = None


class Book(BaseModel):
    key: str
    author_key: Sequence[str]
    author_name: Sequence[str]
    title: str
    language: Sequence[str]
    publish_year: Sequence[int]
    subject: Sequence[str]

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


class HTTPAPIClient:
    _http_client: aiohttp.ClientSession

    def __init__(self) -> None:
        super().__init__()

        self._http_client = aiohttp.ClientSession(BASE_URL)

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

        return params

    async def search_books(self, filter: SearchBooksFilter) -> Sequence[Book]:
        params = self._build_search_books_filters_params(filter)

        async with self._http_client.get("/search.json", params=params) as resp:
            if resp.status != 200:
                raise Exception(f"unexpected status {resp.status}")

            class Response:
                docs: Sequence[Book]

            json: Response = await resp.json()

            books: list[Book] = []

            for doc in json.docs:
                book = Book(
                    key=doc.key,
                    author_key=doc.author_key,
                    author_name=doc.author_name,
                    title=doc.title,
                    language=doc.language,
                    publish_year=doc.publish_year,
                    subject=doc.subject,
                )

                books.append(book)

            return books
