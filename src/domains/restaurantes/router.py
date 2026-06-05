from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from src.app.schemas import CursorPage
from src.domains.restaurantes.schemas import RestauranteCreate, RestauranteResponse
from src.domains.restaurantes.service import RestauranteService

router = APIRouter(prefix="/restaurantes", tags=["restaurantes"])

@router.post("", response_model=RestauranteResponse, status_code=status.HTTP_201_CREATED)
async def create_restaurante(rest_in: RestauranteCreate, service: RestauranteService = Depends()) -> RestauranteResponse:
    """
    Creates a new restaurant profile.
    """
    return await service.create_restaurante(rest_in)

@router.get("/{restaurante_id}", response_model=RestauranteResponse)
async def get_restaurante(restaurante_id: int, service: RestauranteService = Depends()) -> RestauranteResponse:
    """
    Retrieves a restaurant profile by ID.
    """
    return await service.get_restaurante(restaurante_id)

@router.get("", response_model=CursorPage[RestauranteResponse])
async def list_restaurantes(
    limit: int = Query(10, ge=1, le=100),
    cursor: Optional[int] = Query(None),
    service: RestauranteService = Depends()
) -> CursorPage[RestauranteResponse]:
    """
    Lists restaurants using cursor-based pagination.
    """
    return await service.list_restaurantes(limit=limit, cursor=cursor)
