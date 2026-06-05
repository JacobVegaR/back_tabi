from datetime import datetime
from pydantic import BaseModel

class ReservaBase(BaseModel):
    usuario_id: int
    restaurante_id: int
    fecha_hora: datetime

class ReservaCreate(ReservaBase):
    pass

class ReservaResponse(ReservaBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }

class SlotCreate(BaseModel):
    restaurante_id: int
    fecha_hora: datetime
    capacidad_total: int

class SlotResponse(BaseModel):
    id: int
    restaurante_id: int
    fecha_hora: datetime
    capacidad_disponible: int
    capacidad_total: int
    
    model_config = {
        "from_attributes": True
    }
