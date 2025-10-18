from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra="ignore"
    )

    APP_NAME: str = "hermes-2api"
    APP_VERSION: str = "1.0.0"
    DESCRIPTION: str = "一个将 hermes.nousresearch.com 转换为兼容 OpenAI 格式 API 的高性能代理。"

    API_MASTER_KEY: Optional[str] = None
    
    # Hermes 凭证
    HERMES_COOKIE: Optional[str] = None

    API_REQUEST_TIMEOUT: int = 180
    NGINX_PORT: int = 8088

    DEFAULT_MODEL: str = "DeepHermes-3-Llama-3-8B-Preview"
    KNOWN_MODELS: List[str] = ["DeepHermes-3-Llama-3-8B-Preview"]

settings = Settings()
