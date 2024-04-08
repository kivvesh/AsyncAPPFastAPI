import os
from logging import config as logging_config
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict

from . import logger


# Применяем настройки логированияs
logging_config.dictConfig(logger.LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    project_name: str | Any

    # Настройки Uvicorn
    uvicorn_host: str
    uvicorn_port: int

    # Настройки Redis
    redis_host: str
    redis_port: int

    # Настройки Elasticsearch
    elastic_host: str
    elastic_port: int

    model_config = SettingsConfigDict(env_file=f'{BASE_DIR}/.env')


settings = Settings()
