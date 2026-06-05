from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.app.database import Base

class AuthUser(Base):
    __tablename__ = "auth_users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
