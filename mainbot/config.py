import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    discord_bot_token: str
    openai_api_key: str
    openai_model: str
    obsidian_vault_path: str


def load_settings() -> Settings:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    discord_bot_token = os.getenv("DISCORD_BOT_TOKEN", "").strip()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    obsidian_vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "").strip()

    if not token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN is missing. Copy .env.example to .env and add your token."
        )

    return Settings(
        telegram_bot_token=token,
        discord_bot_token=discord_bot_token,
        openai_api_key=api_key,
        openai_model=model,
        obsidian_vault_path=obsidian_vault_path,
    )
