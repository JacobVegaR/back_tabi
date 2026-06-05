from typing import Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.database import get_db
from src.app.errors import AppException
from src.app.schemas import CursorPage
from src.domains.usuarios.repository import UsuarioRepository
from src.domains.usuarios.models import Usuario
from src.domains.usuarios.schemas import UsuarioCreate, UsuarioResponse

class UsuarioService:
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.repository = UsuarioRepository(db)

    async def get_usuario(self, usuario_id: int) -> UsuarioResponse:
        usuario = await self.repository.get_by_id(usuario_id)
        if usuario is None:
            raise AppException(
                status_code=404,
                title="User not found",
                detail=f"The user with ID {usuario_id} does not exist."
            )
        return UsuarioResponse.model_validate(usuario)

    async def create_usuario(self, user_in: UsuarioCreate) -> UsuarioResponse:
        existing = await self.repository.get_by_email(user_in.email)
        if existing is not None:
            raise AppException(
                status_code=400,
                title="User email already exists",
                detail=f"The email {user_in.email} is already in use."
            )
        usuario = Usuario(nombre=user_in.nombre, email=user_in.email)
        created = await self.repository.create(usuario)
        return UsuarioResponse.model_validate(created)

    async def list_usuarios(self, limit: int, cursor: Optional[int]) -> CursorPage[UsuarioResponse]:
        limit_with_extra = limit + 1
        usuarios = await self.repository.list_usuarios(limit=limit_with_extra, cursor_id=cursor)
        
        has_more = len(usuarios) > limit
        if has_more:
            usuarios = usuarios[:limit]
            
        items = [UsuarioResponse.model_validate(u) for u in usuarios]
        next_cursor = str(items[-1].id) if items else None
        
        return CursorPage(
            items=items,
            next_cursor=next_cursor,
            has_more=has_more
        )
