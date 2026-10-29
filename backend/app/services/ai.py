"""Análise de conteúdo (phishing) — OpenRouter com fallback heurístico (ADR-0007)."""

import json
import logging
from typing import Protocol

import httpx
from pydantic import BaseModel, Field

from app.core.config import get_settings
from app.domain.heuristics import heuristic_phishing_score
from app.schemas.classification import EmailPayload

logger = logging.getLogger(__name__)


class ContentAnalysis(BaseModel):
    phishing_score: int = Field(ge=0, le=100)
    indicators: list[str] = Field(default_factory=list)
    justification: str = ""
    source: str = "heuristica"  # llm | heuristica


class ContentAnalyzer(Protocol):
    async def analyze(self, email: EmailPayload) -> ContentAnalysis: ...


class HeuristicAnalyzer:
    """Fallback determinístico quando não há chave de IA."""

    async def analyze(self, email: EmailPayload) -> ContentAnalysis:
        score, hits = heuristic_phishing_score(email.subject, email.body)
        return ContentAnalysis(
            phishing_score=score,
            indicators=hits,
            justification="heurística determinística (sem IA configurada)",
        )


class OpenRouterAnalyzer:
    """IA real via OpenRouter; degrada para heurística em qualquer falha."""

    def __init__(self, api_key: str, model: str, base_url: str):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self._fallback = HeuristicAnalyzer()

    async def analyze(self, email: EmailPayload) -> ContentAnalysis:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "response_format": {"type": "json_object"},
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "Você analisa e-mails em busca de phishing e engenharia social. "
                                    "Responda APENAS um JSON com as chaves: "
                                    '"phishing_score" (inteiro 0–100, onde 0=legítimo e 100=phishing claro), '
                                    '"indicators" (lista com 3 a 5 sinais, cada um uma frase curta e objetiva) e '
                                    '"justification" (uma frase curta). '
                                    "Escreva SEMPRE em português correto, sem gírias nem mistura com outros idiomas, "
                                    "mesmo que o e-mail esteja em inglês ou outro idioma."
                                ),
                            },
                            {
                                "role": "user",
                                "content": (
                                    f"Remetente: {email.sender or '(desconhecido)'}\n"
                                    f"Assunto: {email.subject or '(sem assunto)'}\n"
                                    f"Corpo:\n{email.body[:4000]}"
                                ),
                            },
                        ],
                    },
                )
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                parsed = json.loads(content)
                score = max(0, min(100, int(parsed["phishing_score"])))
                return ContentAnalysis(
                    phishing_score=score,
                    indicators=list(parsed.get("indicators", [])),
                    justification=str(parsed.get("justification", "")),
                    source="llm",
                )
        except Exception as exc:  # noqa: BLE001 — degrada, mas registra o motivo
            logger.warning("OpenRouter indisponível: %s", exc)
            fallback = await self._fallback.analyze(email)
            fallback.justification = f"IA indisponível; {fallback.justification}"
            fallback.source = "heuristica"
            return fallback


def get_content_analyzer() -> ContentAnalyzer:
    settings = get_settings()
    if settings.openrouter_api_key:
        return OpenRouterAnalyzer(
            settings.openrouter_api_key,
            settings.openrouter_model,
            settings.openrouter_base_url,
        )
    return HeuristicAnalyzer()
