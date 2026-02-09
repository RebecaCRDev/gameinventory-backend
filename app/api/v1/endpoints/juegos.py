from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from typing import Optional, List
from decimal import Decimal
from app.models.juego import JuegoOut
from app.services import juego_service
from app.utils.cloudinary_service import upload_image
from app.core.config import settings

router = APIRouter(prefix='/juegos', tags=['Juegos'])


@router.get('', response_model=List[JuegoOut])
def listar_juegos(activos: bool = True):
    '''Listar todos los juegos'''
    return juego_service.listar(activos=activos)


@router.get('/{juego_id}', response_model=JuegoOut)
def obtener_juego(juego_id: int):
    '''Obtener un juego por ID'''
    return juego_service.detalle(juego_id)


@router.post('', response_model=JuegoOut, status_code=status.HTTP_201_CREATED)
async def crear_juego(
    titulo: str = Form(...),
    plataforma: str = Form(...),
    codigo: Optional[str] = Form(None),
    genero: Optional[str] = Form(None),
    precio: Decimal = Form(0.0),
    stock: int = Form(0),
    estado: int = Form(1),
    imagen: Optional[UploadFile] = File(None)
):
    '''Crear un nuevo juego'''
    data = {
        'titulo': titulo,
        'plataforma': plataforma,
        'codigo': codigo,
        'genero': genero,
        'precio': float(precio),
        'stock': stock,
        'estado': estado
    }
    
    if imagen:
        contents = await imagen.read()
        if len(contents) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail='La imagen es muy grande (max 5MB)'
            )
        
        # Crear archivo temporal para Cloudinary
        imagen.file.seek(0)
        imagen_url = upload_image(imagen, folder='juegos')
        
        if imagen_url:
            data['imagen'] = imagen_url
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Error al subir la imagen'
            )
    
    return juego_service.crear(data)


@router.put('/{juego_id}', response_model=JuegoOut)
async def actualizar_juego(
    juego_id: int,
    titulo: Optional[str] = Form(None),
    plataforma: Optional[str] = Form(None),
    codigo: Optional[str] = Form(None),
    genero: Optional[str] = Form(None),
    precio: Optional[Decimal] = Form(None),
    stock: Optional[int] = Form(None),
    estado: Optional[int] = Form(None),
    imagen: Optional[UploadFile] = File(None)
):
    '''Actualizar un juego existente'''
    data = {}
    
    if titulo is not None:
        data['titulo'] = titulo
    if plataforma is not None:
        data['plataforma'] = plataforma
    if codigo is not None:
        data['codigo'] = codigo
    if genero is not None:
        data['genero'] = genero
    if precio is not None:
        data['precio'] = float(precio)
    if stock is not None:
        data['stock'] = stock
    if estado is not None:
        data['estado'] = estado
    
    if imagen:
        contents = await imagen.read()
        if len(contents) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail='La imagen es muy grande (max 5MB)'
            )
        
        imagen.file.seek(0)
        imagen_url = upload_image(imagen, folder='juegos')
        
        if imagen_url:
            data['imagen'] = imagen_url
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Error al subir la imagen'
            )
    
    return juego_service.actualizar(juego_id, data)


@router.delete('/{juego_id}', status_code=status.HTTP_204_NO_CONTENT)
def eliminar_juego(juego_id: int):
    '''Eliminar un juego'''
    juego_service.eliminar(juego_id)
    return None


@router.patch('/{juego_id}/toggle')
def cambiar_estado(juego_id: int):
    '''Cambiar el estado de un juego (activo/inactivo)'''
    return juego_service.toggle_estado(juego_id)
