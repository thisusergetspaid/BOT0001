import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    openai_api_key: str
    openai_model: str


def load_settings() -> Settings:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

    if not token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN is missing. Copy .env.example to .env and add your token."
        )

    return Settings(
        telegram_bot_token=token,
        openai_api_key=api_key,
        openai_model=model,
    )
