from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    qdrant_url: str
    qdrant_api_key: str

    groq_api_key: str

    node_backend_url: str
    frontend_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()