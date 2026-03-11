from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Landscaping ERP API"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://erp:erp@db:5432/erp"
    cors_origins: str = Field(default="http://localhost:3000")
    secret_key: str = "dev-secret-key"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
