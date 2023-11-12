from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_url: str = 'db_URL'
    cloudinary_name: str = 'cloud_name'
    cloudinary_api_key: str = 'api_key'
    cloudinary_api_secret: str = 'api_secret'
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str
    redis_port: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
