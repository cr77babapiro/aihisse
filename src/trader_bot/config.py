from __future__ import annotations

from pathlib import Path
from typing import Optional, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables.

    Uses pydantic-settings to parse and validate environment variables. A
    `.env` file in the project root is supported for local development.
    """

    # General
    environment: Literal["development", "production", "test"] = Field(default="development")
    data_dir: Path = Field(default=Path("data"))

    # Defaults
    default_ticker: str = Field(default="AAPL")
    default_interval: str = Field(default="1m")

    # Brokers
    alpaca_api_key: Optional[str] = Field(default=None, alias="ALPACA_API_KEY")
    alpaca_api_secret: Optional[str] = Field(default=None, alias="ALPACA_API_SECRET")
    alpaca_paper_base_url: str = Field(
        default="https://paper-api.alpaca.markets", alias="ALPACA_PAPER_BASE_URL"
    )

    ib_gateway_host: str = Field(default="127.0.0.1", alias="IB_GATEWAY_HOST")
    ib_gateway_port: int = Field(default=7497, alias="IB_GATEWAY_PORT")

    # Notifications
    telegram_bot_token: Optional[str] = Field(default=None, alias="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: Optional[str] = Field(default=None, alias="TELEGRAM_CHAT_ID")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()  # load on import for convenience
