from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from app.models.usuario import Token
from app.services import auth_service
from app.core.security import decode_access_token

router = APIRouter(prefix='/auth', tags=['Autenticacion'])
security = HTTPBearer()

@router.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    '''
    Login de usuario.
    Credenciales de prueba:
    - Admin: admin@gameinventory.com / admin123
    - Usuario: usuario@gameinventory.com / usuario123
    '''
    result = auth_service.authenticate_user(form_data.username, form_data.password)
    return result

@router.get('/me')
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    '''
    Obtener informacion del usuario autenticado.
    '''
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token invalido o expirado'
        )
    
    return {
        'email': payload.get('sub'),
        'rol': payload.get('rol')
    }