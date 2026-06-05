from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from src.app.schemas import CursorPage
from src.domains.reservas.schemas import ReservaCreate, ReservaResponse, SlotCreate, SlotResponse
from src.domains.reservas.service import ReservaService

router = APIRouter(prefix="/reservas", tags=["reservas"])

@router.post("", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
async def create_reserva(reserva_in: ReservaCreate, service: ReservaService = Depends()) -> ReservaResponse:
    """
    Creates a new reservation with a pessimistic lock on the time slot.
    """
    return await service.create_reserva(reserva_in)

@router.post("/slots", response_model=SlotResponse, status_code=status.HTTP_201_CREATED)
async def create_slot(slot_in: SlotCreate, service: ReservaService = Depends()) -> SlotResponse:
    """
    Creates an availability slot for a restaurant.
    """
    return await service.create_slot(slot_in)

@router.get("/usuario/{usuario_id}", response_model=CursorPage[ReservaResponse])
async def list_reservas_por_usuario(
    usuario_id: int,
    limit: int = Query(10, ge=1, le=100),
    cursor: Optional[int] = Query(None),
    service: ReservaService = Depends()
) -> CursorPage[ReservaResponse]:
    """
    Retrieves reservations for a user with cursor-based pagination.
    """
    return await service.list_reservas_por_usuario(usuario_id=usuario_id, limit=limit, cursor=cursor)
