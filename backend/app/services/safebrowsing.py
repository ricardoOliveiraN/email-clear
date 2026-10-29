"""Validação de links — Google Safe Browsing com fallback passivo (ADR-0007)."""

import logging
from typing import Protocol

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)

THREAT_TYPES = [
    "MALWARE",
    "SOCIAL_ENGINEERING",
    "UNWANTED_SOFTWARE",
    "POTENTIALLY_HARMFUL_APPLICATION",
]


class LinkChecker(Protocol):
    async def check(self, urls: list[str]) -> dict[str, str]:  # url -> safe|dangerous|unknown
        ...


class PassiveLinkChecker:
    """Sem chave de API: não emite veredito (tudo `unknown`)."""

    async def check(self, urls: list[str]) -> dict[str, str]:
        return {url: "unknown" for url in urls}


class SafeBrowsingChecker:
    """Consulta `threatMatches:find`. Só retorna ameaças; não-listado = `safe`."""

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self._fallback = PassiveLinkChecker()

    async def check(self, urls: list[str]) -> dict[str, str]:
        if not urls:
            return {}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    self.base_url,
                    params={"key": self.api_key},
                    json={
                        "client": {"clientId": "email-clear", "clientVersion": "0.1.0"},
                        "threatInfo": {
                            "threatTypes": THREAT_TYPES,
                            "platformTypes": ["ANY_PLATFORM"],
                            "threatEntryTypes": ["URL"],
                            "threatEntries": [{"url": url} for url in urls],
                        },
                    },
                )
                response.raise_for_status()
                matches = response.json().get("matches", [])
            dangerous = {m["threat"]["url"] for m in matches if "threat" in m}
            return {url: ("dangerous" if url in dangerous else "safe") for url in urls}
        except Exception as exc:  # noqa: BLE001 — degrada, mas registra o motivo
            logger.warning("Safe Browsing indisponível: %s", exc)
            return await self._fallback.check(urls)


def get_link_checker() -> LinkChecker:
    settings = get_settings()
    if settings.safebrowsing_api_key:
        return SafeBrowsingChecker(settings.safebrowsing_api_key, settings.safebrowsing_base_url)
    return PassiveLinkChecker()
