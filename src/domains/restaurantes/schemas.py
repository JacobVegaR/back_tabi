from pydantic import BaseModel

class RestauranteBase(BaseModel):
    nombre: str
    direccion: str

class RestauranteCreate(RestauranteBase):
    pass

class RestauranteResponse(RestauranteBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }
