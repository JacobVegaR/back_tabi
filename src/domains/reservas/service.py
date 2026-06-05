from datetime import datetime
from typing import Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.database import get_db
from src.app.errors import AppException
from src.app.schemas import CursorPage
from src.domains.usuarios.service import UsuarioService
from src.domains.restaurantes.service import RestauranteService
from src.domains.reservas.repository import ReservaRepository
from src.domains.reservas.models import Reserva, ReservaSlot
from src.domains.reservas.schemas import ReservaCreate, ReservaResponse, SlotCreate, SlotResponse

class ReservaService:
    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        usuario_service: UsuarioService = Depends(),
        restaurante_service: RestauranteService = Depends()
    ) -> None:
        self.db = db
        self.repository = ReservaRepository(db)
        self.usuario_service = usuario_service
        self.restaurante_service = restaurante_service

    async def create_slot(self, slot_in: SlotCreate) -> SlotResponse:
        await self.restaurante_service.get_restaurante(slot_in.restaurante_id)
        slot = ReservaSlot(
            restaurante_id=slot_in.restaurante_id,
            fecha_hora=slot_in.fecha_hora,
            capacidad_disponible=slot_in.capacidad_total,
            capacidad_total=slot_in.capacidad_total
        )
        created = await self.repository.create_slot(slot)
        return SlotResponse.model_validate(created)

    async def create_reserva(self, reserva_in: ReservaCreate) -> ReservaResponse:
        await self.usuario_service.get_usuario(reserva_in.usuario_id)
        await self.restaurante_service.get_restaurante(reserva_in.restaurante_id)

        slot = await self.repository.get_slot_for_update(
            reserva_in.restaurante_id,
            reserva_in.fecha_hora
        )
        
        if slot is None:
            raise AppException(
                status_code=404,
                title="Slot not found",
                detail="No booking slot exists for this restaurant at the requested time."
            )
            
        if slot.capacidad_disponible <= 0:
            raise AppException(
                status_code=409,
                title="No capacity available",
                detail="The requested booking slot has no remaining capacity."
            )

        slot.capacidad_disponible -= 1
        
        reserva = Reserva(
            usuario_id=reserva_in.usuario_id,
            restaurante_id=reserva_in.restaurante_id,
            fecha_hora=reserva_in.fecha_hora
        )
        created = await self.repository.create_reserva(reserva)
        await self.db.commit()
        return ReservaResponse.model_validate(created)

    async def list_reservas_por_usuario(self, usuario_id: int, limit: int, cursor: Optional[int]) -> CursorPage[ReservaResponse]:
        await self.usuario_service.get_usuario(usuario_id)
        
        limit_with_extra = limit + 1
        reservas = await self.repository.list_reservas_by_usuario(
            usuario_id=usuario_id,
            limit=limit_with_extra,
            cursor_id=cursor
        )
        
        has_more = len(reservas) > limit
        if has_more:
            reservas = reservas[:limit]
            
        items = [ReservaResponse.model_validate(r) for r in reservas]
        next_cursor = str(items[-1].id) if items else None
        
        return CursorPage(
            items=items,
            next_cursor=next_cursor,
            has_more=has_more
        )
