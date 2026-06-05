from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domains.restaurantes.models import Restaurante

class RestauranteRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, restaurante_id: int) -> Optional[Restaurante]:
        stmt = select(Restaurante).where(Restaurante.id == restaurante_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def list_restaurantes(self, limit: int, cursor_id: Optional[int] = None) -> List[Restaurante]:
        stmt = select(Restaurante).order_by(Restaurante.id)
        if cursor_id is not None:
            stmt = stmt.where(Restaurante.id > cursor_id)
        stmt = stmt.limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, restaurante: Restaurante) -> Restaurante:
        self.db.add(restaurante)
        await self.db.commit()
        await self.db.refresh(restaurante)
        return restaurante
