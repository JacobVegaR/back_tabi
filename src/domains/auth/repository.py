from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domains.auth.models import AuthUser

class AuthRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_email(self, email: str) -> Optional[AuthUser]:
        stmt = select(AuthUser).where(AuthUser.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, user: AuthUser) -> AuthUser:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
