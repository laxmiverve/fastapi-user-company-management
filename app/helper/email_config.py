from pydantic_settings import BaseSettings

class EmailSettings(BaseSettings):
    email_host: str
    email_port: int
    email_user: str
    email_password: str

    class Config:
        env_file = ".env"
        extra = "allow"


email_settings = EmailSettings()
