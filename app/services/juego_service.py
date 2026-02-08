from fastapi import HTTPException, status
from app.repositories import juego_repository
import mysql.connector


def listar(activos: bool = True):
    return juego_repository.fetch_all(only_activos=activos)


def detalle(juego_id: int):
    juego = juego_repository.fetch_by_id(juego_id)
    if not juego:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Juego no encontrado'
        )
    return juego


def crear(data: dict):
    _normalizar(data)
    _validar_obligatorios(data)
    
    try:
        new_id = juego_repository.insert(data)
        return detalle(new_id)
    except mysql.connector.Error as e:
        if juego_repository.is_duplicate_codigo_error(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='El codigo (SKU) ya existe'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Error en la base de datos: {str(e)}'
        )


def actualizar(juego_id: int, data: dict):
    detalle(juego_id)
    _normalizar(data)
    
    if 'titulo' in data or 'plataforma' in data:
        _validar_obligatorios(data)
    
    try:
        juego_repository.update(juego_id, data)
        return detalle(juego_id)
    except mysql.connector.Error as e:
        if juego_repository.is_duplicate_codigo_error(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='El codigo (SKU) ya existe'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Error en la base de datos: {str(e)}'
        )


def eliminar(juego_id: int):
    detalle(juego_id)
    juego_repository.delete(juego_id)


def toggle_estado(juego_id: int):
    try:
        nuevo_estado = juego_repository.toggle_estado(juego_id)
        return {'ok': True, 'estado': nuevo_estado}
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Juego no encontrado'
        )


def _normalizar(data: dict):
    if data.get('codigo') is not None:
        data['codigo'] = data['codigo'].strip() or None
    if data.get('genero') is not None:
        data['genero'] = data['genero'].strip() or None
    if 'titulo' in data and data['titulo'] is not None:
        data['titulo'] = data['titulo'].strip()
    if 'plataforma' in data and data['plataforma'] is not None:
        data['plataforma'] = data['plataforma'].strip()


def _validar_obligatorios(data: dict):
    if 'titulo' in data and not data.get('titulo'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='El titulo es obligatorio'
        )
    if 'plataforma' in data and not data.get('plataforma'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='La plataforma es obligatoria'
        )
