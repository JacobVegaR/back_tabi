from fastapi import APIRouter, Depends, status
from src.domains.auth.schemas import UserCreate, UserResponse
from src.domains.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, service: AuthService = Depends()) -> UserResponse:
    """
    Registers a new user and returns their profile.
    """
    return await service.register(user_in)
