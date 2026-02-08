from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class JuegoBase(BaseModel):
    codigo: Optional[str] = Field(None, max_length=50)
    titulo: str = Field(min_length=1, max_length=200)
    plataforma: str = Field(min_length=1, max_length=50)
    genero: Optional[str] = Field(None, max_length=80)
    precio: Decimal = Field(default=0.0, ge=0)
    stock: int = Field(default=0, ge=0)
    estado: int = Field(default=1, ge=0, le=1)


class JuegoCreate(JuegoBase):
    pass


class JuegoUpdate(BaseModel):
    codigo: Optional[str] = Field(None, max_length=50)
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    plataforma: Optional[str] = Field(None, min_length=1, max_length=50)
    genero: Optional[str] = Field(None, max_length=80)
    precio: Optional[Decimal] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)
    estado: Optional[int] = Field(None, ge=0, le=1)


class JuegoOut(JuegoBase):
    id: int
    imagen: Optional[str] = None

    class Config:
        from_attributes = True
