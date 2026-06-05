from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from src.app.schemas import CursorPage
from src.domains.usuarios.schemas import UsuarioCreate, UsuarioResponse
from src.domains.usuarios.service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def create_usuario(usuario_in: UsuarioCreate, service: UsuarioService = Depends()) -> UsuarioResponse:
    """
    Creates a new user profile.
    """
    return await service.create_usuario(usuario_in)

@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(usuario_id: int, service: UsuarioService = Depends()) -> UsuarioResponse:
    """
    Retrieves a user profile by ID.
    """
    return await service.get_usuario(usuario_id)

@router.get("", response_model=CursorPage[UsuarioResponse])
async def list_usuarios(
    limit: int = Query(10, ge=1, le=100),
    cursor: Optional[int] = Query(None),
    service: UsuarioService = Depends()
) -> CursorPage[UsuarioResponse]:
    """
    Lists user profiles using cursor-based pagination.
    """
    return await service.list_usuarios(limit=limit, cursor=cursor)
