from app.core.exceptions import BookNotFoundError
from app.data.books import BookRepository
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


async def list_books(
    books: BookRepository,
    user_id: int,
    *,
    offset: int,
    limit: int,
) -> list[Book]:
    return await books.list_for_user(user_id, offset=offset, limit=limit)


async def get_book(books: BookRepository, user_id: int, book_id: int) -> Book:
    book = await books.get_for_user(user_id, book_id)
    if book is None:
        raise BookNotFoundError
    return book


async def create_book(books: BookRepository, user_id: int, data: BookCreate) -> Book:
    book = Book(
        user_id=user_id,
        title=data.title,
        author=data.author,
        description=data.description,
    )
    return await books.add(book)


async def update_book(
    books: BookRepository,
    user_id: int,
    book_id: int,
    data: BookUpdate,
) -> Book:
    book = await get_book(books, user_id, book_id)
    changes = data.model_dump(exclude_unset=True)
    if not changes:
        return book
    return await books.apply_update(book, changes)


async def delete_book(books: BookRepository, user_id: int, book_id: int) -> None:
    book = await get_book(books, user_id, book_id)
    await books.delete(book)
