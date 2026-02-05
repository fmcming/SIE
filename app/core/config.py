from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "dev"
    model_registry_url: str = "http://localhost:9000"
    default_model_version: str = "yolo-stub-v0"
    image_max_size: int = 1280


settings = Settings()
