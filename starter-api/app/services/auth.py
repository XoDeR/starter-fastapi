import asyncio

from app.core.exceptions import EmailAlreadyRegisteredError, InvalidCredentialsError
from app.core.security import (
    create_access_token,
    dummy_password_hash,
    hash_password,
    verify_password,
)
from app.data.users import UserRepository
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest


async def register_user(
    users: UserRepository,
    data: RegisterRequest,
) -> tuple[str, User]:
    existing = await users.get_by_email(data.email)
    if existing is not None:
        raise EmailAlreadyRegisteredError

    hashed = await asyncio.to_thread(hash_password, data.password)
    user = User(name=data.name, email=data.email, password=hashed)
    user = await users.add(user)
    if user.id is None:
        raise RuntimeError("User id was not assigned")
    return create_access_token(user.id), user


async def authenticate_user(
    users: UserRepository,
    data: LoginRequest,
) -> tuple[str, User]:
    user = await users.get_by_email(data.email)
    hashed = user.password if user is not None else dummy_password_hash()
    password_ok = await asyncio.to_thread(verify_password, data.password, hashed)
    if user is None or user.id is None or not password_ok:
        raise InvalidCredentialsError
    return create_access_token(user.id), user
