from fastapi import APIRouter, status
from typing import List
from app.models.usuario import UsuarioOut, UsuarioCreate, UsuarioUpdate
from app.services import usuario_service

router = APIRouter(prefix='/usuarios', tags=['Usuarios'])


@router.get('', response_model=List[UsuarioOut])
def listar_usuarios():
    '''
    Listar todos los usuarios.
    '''
    return usuario_service.listar()


@router.get('/{usuario_id}', response_model=UsuarioOut)
def obtener_usuario(usuario_id: int):
    '''
    Obtener un usuario por ID.
    '''
    return usuario_service.detalle(usuario_id)


@router.post('', response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate):
    '''
    Crear un nuevo usuario.
    '''
    return usuario_service.crear(usuario.model_dump())


@router.put('/{usuario_id}', response_model=UsuarioOut)
def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate):
    '''
    Actualizar un usuario existente.
    '''
    data = usuario.model_dump(exclude_unset=True)
    return usuario_service.actualizar(usuario_id, data)


@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(usuario_id: int):
    '''
    Eliminar un usuario.
    '''
    usuario_service.eliminar(usuario_id)
    return None
