from datetime import datetime

from pydantic import BaseModel

UserID = int


class User(BaseModel):
    id: UserID
    login: str
    created_at: datetime
