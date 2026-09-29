from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, Text
from sqlmodel import Field, SQLModel

from app.core.time import utcnow


def _big_int() -> BigInteger:
    return BigInteger().with_variant(Integer, "sqlite")


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: int | None = Field(default=None, primary_key=True, sa_type=_big_int())
    user_id: int = Field(foreign_key="users.id", index=True, sa_type=_big_int())
    title: str = Field(max_length=255)
    author: str = Field(max_length=255)
    description: str | None = Field(default=None, sa_type=Text)
    created_at: datetime = Field(default_factory=utcnow, sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(default_factory=utcnow, sa_type=DateTime(timezone=True))
