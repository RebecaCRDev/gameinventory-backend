from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title='GameInventory API',
    description='API REST para gestion de inventario de videojuegos',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redoc'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

uploads_path = Path(settings.UPLOAD_DIR)
uploads_path.mkdir(parents=True, exist_ok=True)
app.mount('/uploads', StaticFiles(directory='uploads'), name='uploads')

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get('/')
def root():
    return {
        'message': 'GameInventory API',
        'version': '1.0.0',
        'docs': '/docs',
        'status': 'online'
    }
