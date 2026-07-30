"""
Sentinel — OpenAI & Vector Store Settings
Loads and validates settings for OpenAI, FAISS, and model details.
"""
from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAISettings(BaseSettings):
    """Configuration settings for Sentinel OpenAI and FAISS integration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ─── OpenAI API ────────────────────────────────────────────
    OPENAI_API_KEY: str = Field(..., description="OpenAI API key")
    OPENAI_EMBEDDING_MODEL: str = Field(default="text-embedding-ada-002")
    OPENAI_CHAT_MODEL: str = Field(default="gpt-4")
    OPENAI_TEMPERATURE: float = Field(default=0.2, ge=0.0, le=2.0)
    OPENAI_MAX_TOKENS: int = Field(default=1024, ge=1)

    # ─── FAISS Vector Store ────────────────────────────────────
    FAISS_INDEX_PATH: str = Field(default="./data/faiss_index")
    FAISS_INDEX_NAME: str = Field(default="sentinel_support_index")
    FAISS_TOP_K: int = Field(default=5, ge=1)
    EMBEDDING_DIMENSION: int = Field(default=1536)

    # ─── App Settings ──────────────────────────────────────────
    APP_NAME: str = Field(default="Sentinel Support Platform")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(default="INFO")

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid:
            raise ValueError(f"LOG_LEVEL must be one of {valid}")
        return v.upper()

    @property
    def faiss_dir(self) -> Path:
        return Path(self.FAISS_INDEX_PATH)


@lru_cache(maxsize=1)
def get_openai_settings() -> OpenAISettings:
    """Return cached OpenAI settings instance."""
    return OpenAISettings()


# Module-level instance
openai_settings = get_openai_settings()
