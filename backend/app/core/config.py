from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "email-clear"
    environment: str = "development"

    database_url: str = "postgresql+asyncpg://emailclear:emailclear@localhost:5432/emailclear"

    # ADR-0014 — token de instalação emitido pelo servidor (HMAC)
    install_token_secret: str = "dev-secret-change-me"
    # limita emissão de tokens por IP (anti-abuso — ADR-0014 §5)
    install_rate_limit_per_ip: int = 5
    install_rate_limit_window_seconds: int = 86400

    # ADR-0005 — quota de validações por instalação/dia (best-effort)
    validate_daily_quota: int = 100

    # ADR-0007 — IA de conteúdo (OpenRouter)
    openrouter_api_key: str = ""
    openrouter_model: str = "openai/gpt-4o-mini"
    openrouter_base_url: str = "https://openrouter.ai/api/v1/chat/completions"

    # ADR-0007 — validação de links (Google Safe Browsing)
    safebrowsing_api_key: str = ""
    safebrowsing_base_url: str = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

    # ADR-0015 — TTL do cache L2 por hash de conteúdo (segundos)
    cache_ttl_seconds: int = 86400


@lru_cache
def get_settings() -> Settings:
    return Settings()
