# GameInventory API

API REST para gestión de inventario de videojuegos desarrollada con FastAPI.

## Características

- ? Autenticación JWT
- ? CRUD de juegos con imágenes
- ? CRUD de usuarios
- ? Roles (admin/usuario)
- ? Búsqueda y filtros
- ? Documentación automática (Swagger)

## Requisitos

- Python 3.8+
- MySQL/MariaDB
- pip

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual:
```
python -m venv .venv
.venv\Scripts\activate
```

3. Instalar dependencias:
```
pip install -r requirements.txt
```

4. Configurar .env (copiar de .env.black)

5. Crear base de datos en MySQL

6. Ejecutar el servidor:
```
uvicorn main:app --reload
```

## Documentación

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Credenciales de prueba

- Admin: admin@gameinventory.com / admin123
- Usuario: usuario@gameinventory.com / usuario123

## Endpoints principales

### Autenticación
- POST /api/auth/login - Login
- GET /api/auth/me - Usuario actual

### Juegos
- GET /api/juegos - Listar juegos
- GET /api/juegos/{id} - Obtener juego
- POST /api/juegos - Crear juego
- PUT /api/juegos/{id} - Actualizar juego
- DELETE /api/juegos/{id} - Eliminar juego
- PATCH /api/juegos/{id}/toggle - Cambiar estado

### Usuarios
- GET /api/usuarios - Listar usuarios
- GET /api/usuarios/{id} - Obtener usuario
- POST /api/usuarios - Crear usuario
- PUT /api/usuarios/{id} - Actualizar usuario
- DELETE /api/usuarios/{id} - Eliminar usuario
