from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str = Field(default= 'postgresql+asyncpg://santander:santander@localhost/santander')


settings = Settings()
