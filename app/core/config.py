from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "gameinventory"
    DB_PORT: int = 3306

# Cloudinary
    CLOUDINARY_CLOUD_NAME: str = "drbtinf6a"
    CLOUDINARY_API_KEY: str = "233317843164278"
    CLOUDINARY_API_SECRET: str = "QjduXmM8IKMEBAgvVk-FneFWAYc"

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # App
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api"

    # Upload
    UPLOAD_DIR: str = "uploads/juegos"
    MAX_FILE_SIZE: int = 5242880  # 5MB

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
