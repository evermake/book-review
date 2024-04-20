from pydantic import BaseModel

from datetime import date


BookID = str
AuthorID = str


class Author(BaseModel):
    id: AuthorID
    name: str


class BookPreview(BaseModel):
    id: BookID
    title: str
    cover_key: str
    author: Author
    first_publishment_date: date
    subjects: list[str]
    languages: list[str]


class Book(BookPreview):
    synopsis: str
