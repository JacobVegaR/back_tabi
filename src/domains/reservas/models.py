from datetime import datetime
from sqlalchemy import Integer, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.app.database import Base

class ReservaSlot(Base):
    __tablename__ = "reserva_slots"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    restaurante_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    fecha_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    capacidad_disponible: Mapped[int] = mapped_column(Integer, nullable=False)
    capacidad_total: Mapped[int] = mapped_column(Integer, nullable=False)
    
    __table_args__ = (
        UniqueConstraint("restaurante_id", "fecha_hora", name="uq_restaurante_slot"),
    )

class Reserva(Base):
    __tablename__ = "reservas"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    restaurante_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    fecha_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False)
