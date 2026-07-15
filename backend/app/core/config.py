from pydantic_settings import BaseSettings
from pathlib import Path

env_path = Path(__file__).parent.parent.parent / ".env"


class Settings(BaseSettings):
    PORT: int
    HOST: str

    class Config:
        env_file = env_path


settings = Settings()
__all__ = ["settings"]
