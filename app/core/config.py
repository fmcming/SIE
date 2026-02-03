from pydantic import BaseModel


class Settings(BaseModel):
    env: str = "dev"
    model_registry_url: str = "http://localhost:9000"


settings = Settings()
