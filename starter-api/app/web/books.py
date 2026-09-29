from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.exceptions import BookNotFoundError
from app.data.books import BookRepository
from app.models.user import User
from app.schemas.book import BookCreate, BookPublic, BookUpdate
from app.services import books as book_service
from app.web.deps import get_book_repository, get_current_user, require_user_id

router = APIRouter(prefix="/books", tags=["books"])


def _user_id(current_user: User) -> int:
    return require_user_id(current_user)


@router.get("", response_model=list[BookPublic])
async def list_books(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    books: BookRepository = Depends(get_book_repository),
) -> list[BookPublic]:
    rows = await book_service.list_books(
        books,
        _user_id(current_user),
        offset=offset,
        limit=limit,
    )
    return [BookPublic.model_validate(row) for row in rows]


@router.post("", response_model=BookPublic, status_code=status.HTTP_201_CREATED)
async def create_book(
    body: BookCreate,
    current_user: User = Depends(get_current_user),
    books: BookRepository = Depends(get_book_repository),
) -> BookPublic:
    book = await book_service.create_book(books, _user_id(current_user), body)
    return BookPublic.model_validate(book)


@router.get("/{book_id}", response_model=BookPublic)
async def get_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    books: BookRepository = Depends(get_book_repository),
) -> BookPublic:
    try:
        book = await book_service.get_book(books, _user_id(current_user), book_id)
    except BookNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found") from None
    return BookPublic.model_validate(book)


@router.patch("/{book_id}", response_model=BookPublic)
async def update_book(
    book_id: int,
    body: BookUpdate,
    current_user: User = Depends(get_current_user),
    books: BookRepository = Depends(get_book_repository),
) -> BookPublic:
    try:
        book = await book_service.update_book(books, _user_id(current_user), book_id, body)
    except BookNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found") from None
    return BookPublic.model_validate(book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    books: BookRepository = Depends(get_book_repository),
) -> None:
    try:
        await book_service.delete_book(books, _user_id(current_user), book_id)
    except BookNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found") from None
