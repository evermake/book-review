from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .book import BookID
from .user import UserID


class Review(BaseModel):
    user_id: UserID
    book_id: BookID
    rating: int
    commentary: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
