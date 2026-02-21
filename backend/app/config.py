from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ANTHROPIC_API_KEY: str
    DATA_DIR: str = "./data"
    MODEL_NAME: str = "claude-sonnet-4-20250514"
    MAX_CONVERSATION_TURNS: int = 20
    LOG_LEVEL: str = "INFO"


settings = Settings()
