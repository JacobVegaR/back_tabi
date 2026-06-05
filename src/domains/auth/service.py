from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.database import get_db
from src.app.errors import AppException
from src.domains.auth.repository import AuthRepository
from src.domains.auth.models import AuthUser
from src.domains.auth.schemas import UserCreate, UserResponse

class AuthService:
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.repository = AuthRepository(db)

    async def register(self, user_in: UserCreate) -> UserResponse:
        existing = await self.repository.get_by_email(user_in.email)
        if existing is not None:
            raise AppException(
                status_code=400,
                title="Email already exists",
                detail=f"The email address {user_in.email} is already registered."
            )
        
        hashed_password = f"dummy_hash_{user_in.password}"
        user = AuthUser(email=user_in.email, hashed_password=hashed_password)
        created = await self.repository.create(user)
        return UserResponse.model_validate(created)
