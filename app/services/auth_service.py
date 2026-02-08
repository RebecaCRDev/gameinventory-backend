from datetime import timedelta
from fastapi import HTTPException, status
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.repositories import usuario_repository


def authenticate_user(email: str, password: str):
    # Buscar usuario por email
    user = usuario_repository.fetch_by_email(email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Email o contrasena incorrectos'
        )
    
    # Verificar si esta activo
    if user['estado'] != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Usuario inactivo'
        )
    
    # Verificar contrasena
    if not verify_password(password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Email o contrasena incorrectos'
        )
    
    # Crear token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user['email'], 'rol': user['rol']},
        expires_delta=access_token_expires
    )
    
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user': {
            'id': user['id'],
            'nombre': user['nombre'],
            'email': user['email'],
            'rol': user['rol']
        }
    }
