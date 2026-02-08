from fastapi import HTTPException, status
from app.repositories import usuario_repository
from app.core.security import get_password_hash
import mysql.connector


def listar():
    return usuario_repository.fetch_all()


def detalle(usuario_id: int):
    usuario = usuario_repository.fetch_by_id(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuario no encontrado'
        )
    return usuario


def crear(data: dict):
    existing = usuario_repository.fetch_by_email(data['email'])
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='El email ya esta registrado'
        )
    
    data['password'] = get_password_hash(data['password'])
    
    try:
        new_id = usuario_repository.insert(data)
        return detalle(new_id)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Error en la base de datos: {str(e)}'
        )


def actualizar(usuario_id: int, data: dict):
    detalle(usuario_id)
    
    if 'email' in data:
        existing = usuario_repository.fetch_by_email(data['email'])
        if existing and existing['id'] != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='El email ya esta registrado'
            )
    
    if 'password' in data:
        data['password'] = get_password_hash(data['password'])
    
    try:
        usuario_repository.update(usuario_id, data)
        return detalle(usuario_id)
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Error en la base de datos: {str(e)}'
        )


def eliminar(usuario_id: int):
    detalle(usuario_id)
    usuario_repository.delete(usuario_id)
