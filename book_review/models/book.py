from datetime import date
from typing import Optional, Sequence

from pydantic import BaseModel

BookID = str
AuthorID = str
CoverID = int


class Author(BaseModel):
    id: AuthorID
    name: str


class BookPreview(BaseModel):
    id: BookID
    title: str
    cover_id: Optional[CoverID] = None
    authors: Sequence[Author] = []
    first_publishment_date: Optional[date] = None
    subjects: Sequence[str] = []
    languages: Sequence[str] = []


class Book(BaseModel):
    id: BookID
    title: str
    description: Optional[str] = None
    covers: Sequence[CoverID] = []
    subjects: Sequence[str] = []
    author_id: Optional[AuthorID] = None
