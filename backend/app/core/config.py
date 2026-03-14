from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "MT5 Trading Robot API"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    aes_key: str = "0123456789abcdef0123456789abcdef"  # 32-byte key


settings = Settings()
