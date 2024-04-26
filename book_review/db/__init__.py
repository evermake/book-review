from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

from book_review.models.book import BookID
from book_review.models.user import UserID


async def create_all(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(TableUsers.metadata.create_all)
        await connection.run_sync(TableReviews.metadata.create_all)


class Base(DeclarativeBase):
    pass


class TableUsers(Base):
    __tablename__ = "users"

    id: Mapped[UserID] = mapped_column(primary_key=True, index=True)
    login: Mapped[str] = mapped_column(String(30), unique=True)
    password_hash: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())


class TableReviews(Base):
    __tablename__ = "reviews"

    user_id: Mapped[UserID] = mapped_column(
        ForeignKey(f"{TableUsers.__tablename__}.id"), primary_key=True
    )
    book_id: Mapped[BookID] = mapped_column(String(), primary_key=True)

    rating: Mapped[int] = mapped_column(CheckConstraint("rating between 1 and 10"))
    commentary: Mapped[Optional[str]] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column()
