from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "postgresql+psycopg://localhost/energy_atlas_dev"
    owid_source_url: str = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
    cors_origins: str = "http://localhost:5175"


settings = Settings()
