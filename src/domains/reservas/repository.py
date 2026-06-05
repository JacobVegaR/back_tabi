from datetime import datetime
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domains.reservas.models import Reserva, ReservaSlot

class ReservaRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_slot_for_update(self, restaurante_id: int, fecha_hora: datetime) -> Optional[ReservaSlot]:
        stmt = (
            select(ReservaSlot)
            .where(
                ReservaSlot.restaurante_id == restaurante_id,
                ReservaSlot.fecha_hora == fecha_hora
            )
            .with_for_update()
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create_slot(self, slot: ReservaSlot) -> ReservaSlot:
        self.db.add(slot)
        await self.db.commit()
        await self.db.refresh(slot)
        return slot

    async def create_reserva(self, reserva: Reserva) -> Reserva:
        self.db.add(reserva)
        await self.db.flush()
        await self.db.refresh(reserva)
        return reserva

    async def list_reservas_by_usuario(self, usuario_id: int, limit: int, cursor_id: Optional[int] = None) -> List[Reserva]:
        stmt = select(Reserva).where(Reserva.usuario_id == usuario_id).order_by(Reserva.id)
        if cursor_id is not None:
            stmt = stmt.where(Reserva.id > cursor_id)
        stmt = stmt.limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
