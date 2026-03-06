from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    DATABASE_TEST_URL: str
    EMAIL_API_URL: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_ARENA_MANAGER_QUEUE: str
    RABBITMQ_ARENA_MANAGER_EXCHANGE: str
    RABBITMQ_ARENA_MANAGER_ROUTING_KEY: str

    @property
    def RABBITMQ_URL(self):
        return f"amqp://{self.RABBITMQ_USERNAME}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
