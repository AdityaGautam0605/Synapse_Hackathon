from pydantic import BaseModel


class Settings(BaseModel):
    API_V1_PREFIX: str = "/api/v1"
    VERSION: str = "v1"

    JWT_SECRET_KEY: str = "change-me-to-a-long-random-string"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24


settings = Settings()