from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.app.database import Base

class Restaurante(Base):
    __tablename__ = "restaurantes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    direccion: Mapped[str] = mapped_column(String(255), nullable=False)
