from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String
from sqlmodel import Field, SQLModel

from app.core.time import utcnow


def _big_int() -> BigInteger:
    # SQLite only autoincrements INTEGER primary keys. Postgres keeps bigint.
    return BigInteger().with_variant(Integer, "sqlite")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True, sa_type=_big_int())
    name: str = Field(max_length=255)
    email: str = Field(max_length=255, unique=True, index=True)
    email_verified_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
    )
    password: str = Field(max_length=255)
    remember_token: str | None = Field(default=None, max_length=100, sa_type=String(100))
    created_at: datetime = Field(default_factory=utcnow, sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(default_factory=utcnow, sa_type=DateTime(timezone=True))
