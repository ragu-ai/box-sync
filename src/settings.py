from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Ragu Sync"
    debug: bool = False
    database_name: str = "ragu_sync_db"
    database_user: str = "ragu_user"
    database_password: str = "your_password"
    database_host: str = "localhost"
    database_port: int = 3306

    class Config:
        env_file = ".env"


settings = Settings()
