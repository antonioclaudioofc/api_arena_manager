from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    DATABASE_TEST_URL: str
    NOTIFY_API_URL: str
    NOTIFY_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
