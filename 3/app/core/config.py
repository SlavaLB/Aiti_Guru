from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    app_title: str = Field(..., validation_alias='APP_TITLE')
    app_author: str = Field(..., validation_alias='APP_AUTHOR')
    secret: str = Field('SECRET', validation_alias='SECRET_KEY')

    database_url: str = Field(..., validation_alias='DATABASE_URL')

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / '.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )


settings = Settings()
