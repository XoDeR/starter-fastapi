from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.time import utcnow
from app.models.book import Book


class BookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_for_user(self, user_id: int, *, offset: int, limit: int) -> list[Book]:
        statement = (
            select(Book)
            .where(Book.user_id == user_id)
            .order_by(Book.id.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.exec(statement)
        return list(result.all())

    async def get_for_user(self, user_id: int, book_id: int) -> Book | None:
        statement = select(Book).where(Book.id == book_id, Book.user_id == user_id)
        result = await self.session.exec(statement)
        return result.first()

    async def add(self, book: Book) -> Book:
        now = utcnow()
        book.created_at = now
        book.updated_at = now
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def apply_update(self, book: Book, changes: dict[str, object]) -> Book:
        for key, value in changes.items():
            setattr(book, key, value)
        book.updated_at = utcnow()
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def delete(self, book: Book) -> None:
        await self.session.delete(book)
        await self.session.commit()
