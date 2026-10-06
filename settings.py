from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    MAIL_HOST: str

    MAIL_PORT: int = 2525

    MAIL_USERNAME: str

    MAIL_PASSWORD: str

    MAIL_FROM: str

    MAIL_FROM_NAME: str = "Blog Management API"

    class Config:
        env_file = ".env"


settings = Settings()