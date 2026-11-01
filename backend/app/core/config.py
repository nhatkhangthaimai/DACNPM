import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "HireSense AI - Smart Recruitment Platform"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "hiresense_ai_super_secret_jwt_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/hiresense_db"
    SYNC_DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/hiresense_db"
    
    # Gemini AI
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"
    EMBEDDING_MODEL: str = "models/text-embedding-004"
    
    # Storage
    UPLOAD_DIR: str = os.path.join(os.getcwd(), "uploads")
    MAX_FILE_SIZE_MB: int = 10
    
    # CORS
    BACKEND_CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str) -> str:
        if isinstance(v, str):
            if v.startswith("postgres://"):
                return v.replace("postgres://", "postgresql+asyncpg://", 1)
            elif v.startswith("postgresql://") and not v.startswith("postgresql+asyncpg://"):
                return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.strip() == "*":
                return ["*"]
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
