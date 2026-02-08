from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    email: EmailStr
    rol: str = Field(default="usuario", pattern="^(admin|usuario)$")


class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=6)


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    rol: Optional[str] = Field(None, pattern="^(admin|usuario)$")
    password: Optional[str] = Field(None, min_length=6)
    estado: Optional[int] = Field(None, ge=0, le=1)


class UsuarioOut(UsuarioBase):
    id: int
    estado: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    rol: Optional[str] = None
