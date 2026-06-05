from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domains.usuarios.models import Usuario

class UsuarioRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        stmt = select(Usuario).where(Usuario.id == usuario_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[Usuario]:
        stmt = select(Usuario).where(Usuario.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def list_usuarios(self, limit: int, cursor_id: Optional[int] = None) -> List[Usuario]:
        stmt = select(Usuario).order_by(Usuario.id)
        if cursor_id is not None:
            stmt = stmt.where(Usuario.id > cursor_id)
        stmt = stmt.limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        await self.db.commit()
        await self.db.refresh(usuario)
        return usuario
