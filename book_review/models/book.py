from datetime import date
from typing import Optional, Sequence

from pydantic import BaseModel

BookID = str
AuthorID = str


class Author(BaseModel):
    id: AuthorID
    name: str


class BookPreview(BaseModel):
    id: BookID
    title: str
    authors: Sequence[Author] = []
    first_publishment_date: Optional[date] = None
    subjects: list[str] = []
    languages: list[str] = []


class Book(BookPreview):
    synopsis: str
