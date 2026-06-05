from typing import Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.database import get_db
from src.app.errors import AppException
from src.app.schemas import CursorPage
from src.domains.restaurantes.repository import RestauranteRepository
from src.domains.restaurantes.models import Restaurante
from src.domains.restaurantes.schemas import RestauranteCreate, RestauranteResponse

class RestauranteService:
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.repository = RestauranteRepository(db)

    async def get_restaurante(self, restaurante_id: int) -> RestauranteResponse:
        restaurante = await self.repository.get_by_id(restaurante_id)
        if restaurante is None:
            raise AppException(
                status_code=404,
                title="Restaurant not found",
                detail=f"The restaurant with ID {restaurante_id} does not exist."
            )
        return RestauranteResponse.model_validate(restaurante)

    async def create_restaurante(self, rest_in: RestauranteCreate) -> RestauranteResponse:
        restaurante = Restaurante(nombre=rest_in.nombre, direccion=rest_in.direccion)
        created = await self.repository.create(restaurante)
        return RestauranteResponse.model_validate(created)

    async def list_restaurantes(self, limit: int, cursor: Optional[int]) -> CursorPage[RestauranteResponse]:
        limit_with_extra = limit + 1
        restaurantes = await self.repository.list_restaurantes(limit=limit_with_extra, cursor_id=cursor)
        
        has_more = len(restaurantes) > limit
        if has_more:
            restaurantes = restaurantes[:limit]
            
        items = [RestauranteResponse.model_validate(r) for r in restaurantes]
        next_cursor = str(items[-1].id) if items else None
        
        return CursorPage(
            items=items,
            next_cursor=next_cursor,
            has_more=has_more
        )
