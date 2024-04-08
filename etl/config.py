from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # PostgreSQL settings
    postgres_user: str = Field(
        default='app',
        json_schema_extra={'env': 'POSTGRES_USER'}
    )
    postgres_db: str = Field(
        default='movies_database',
        json_schema_extra={'env': 'POSTGRES_DB'}
    )
    postgres_password: str = Field(
        default='123qwe',
        json_schema_extra={'env': 'POSTGRES_PASSWORD'}
    )
    postgres_host: str = Field(
        default='postgres',
        json_schema_extra={'env': 'POSTGRES_HOST'}
    )
    postgres_port: int = Field(
        default=5432,
        json_schema_extra={'env': 'POSTGRES_PORT'}
    )
    postgres_options: str = Field(
        default='-c search_path=content',
        json_schema_extra={'env': 'POSTGRES_OPTIONS'}
    )

    # Elasticsearch settings
    elastic_host: str = Field(
        default='elsaticsearch',
        json_schema_extra={'env': 'ELASTIC_HOST'}
    )
    elastic_port: int = Field(
        default=9200,
        json_schema_extra={'env': 'ELASTIC_PORT'}
    )


settings = Settings()
