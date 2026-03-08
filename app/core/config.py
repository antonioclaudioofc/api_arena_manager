from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    DATABASE_TEST_URL: str
    EMAIL_API_URL: str
    RABBITMQ_URL: str
    RABBITMQ_ARENA_MANAGER_QUEUE: str
    RABBITMQ_ARENA_MANAGER_EXCHANGE: str
    RABBITMQ_ARENA_MANAGER_ROUTING_KEY: str


    class Config:
        env_file = ".env"


settings = Settings()
