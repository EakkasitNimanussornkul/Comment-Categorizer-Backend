# Loads environment variables (DB URL, Secret Keys)
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: SecretStr 

    # Modern Pydantic v2 way to tell it to read the .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Create the globally available settings object
settings = Settings()