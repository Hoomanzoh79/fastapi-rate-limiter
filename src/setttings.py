from pydantic_settings import BaseSettings

from src import BASE_DIR

class Settings(BaseSettings):
    REDIS_URL: str 
    # default rate limit (example): 100 requests per 60 seconds
    RATE_LIMIT_REQUESTS: int 
    RATE_LIMIT_WINDOW_SECONDS: int 

    class Config:
        env_file = BASE_DIR.joinpath(".env")

settings = Settings()
