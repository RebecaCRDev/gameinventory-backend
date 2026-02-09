import cloudinary
import cloudinary.uploader
from app.core.config import settings
import io

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

def upload_image(file, folder='juegos'):
    '''Sube una imagen a Cloudinary'''
    try:
        # Leer el contenido del archivo
        file_content = file.file.read()
        file.file.seek(0)
        
        result = cloudinary.uploader.upload(
            file_content,
            folder=folder,
            resource_type='image'
        )
        return result['secure_url']
    except Exception as e:
        print(f'Error al subir imagen: {e}')
        return None

def delete_image(public_id):
    '''Elimina una imagen de Cloudinary'''
    try:
        cloudinary.uploader.destroy(public_id)
    except Exception as e:
        print(f'Error al eliminar imagen: {e}')
