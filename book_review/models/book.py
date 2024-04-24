from datetime import date
from typing import Optional, Sequence

from pydantic import BaseModel

BookID = str
AuthorID = str


class Author(BaseModel):
    id: AuthorID
    name: str


class Book(BaseModel):
    id: BookID
    title: str
    authors: Sequence[Author] = []
    first_publishment_date: Optional[date] = None
    subjects: Sequence[str] = []
    languages: Sequence[str] = []
