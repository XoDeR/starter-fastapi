from fastapi import APIRouter, Depends, HTTPException, status

from app.core.exceptions import EmailAlreadyRegisteredError, InvalidCredentialsError
from app.data.users import UserRepository
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.services import auth as auth_service
from app.web.deps import get_current_user, get_user_repository

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest,
    users: UserRepository = Depends(get_user_repository),
) -> TokenResponse:
    try:
        token, user = await auth_service.register_user(users, body)
    except EmailAlreadyRegisteredError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered") from None
    return TokenResponse(token=token, user=UserPublic.model_validate(user))


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    users: UserRepository = Depends(get_user_repository),
) -> TokenResponse:
    try:
        token, user = await auth_service.authenticate_user(users, body)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None
    return TokenResponse(token=token, user=UserPublic.model_validate(user))


@router.get("/user", response_model=UserPublic)
async def read_current_user(current_user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic.model_validate(current_user)
