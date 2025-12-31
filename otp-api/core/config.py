from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    smtp_from_name: str
    smtp_from_email: str

    class Config:
        env_file = ".env"

settings = Settings()
