"""Heurística determinística barata — fallback quando não há chave de IA (ADR-0007).

Intencionalmente simples: apenas um ponto de partida calibrável, NÃO a fonte
principal de classificação de conteúdo.
"""

SUSPICIOUS_KEYWORDS = [
    "urgente",
    "urgent",
    "senha",
    "password",
    "verifique sua conta",
    "verify your account",
    "suspens",
    "suspended",
    "clique aqui",
    "click here",
    "cartão",
    "card number",
    "login",
    "confirme seus dados",
    "bloqueado",
    "locked",
    "prêmio",
    "prize",
    "loteria",
    "lottery",
]


def heuristic_phishing_score(subject: str | None, body: str | None) -> tuple[int, list[str]]:
    text = f"{subject or ''} {body or ''}".lower()
    hits = [kw for kw in SUSPICIOUS_KEYWORDS if kw in text]
    # 15 pontos por palavra, teto de 100 (0–100, calibrado por ADR-0007)
    score = min(100, len(hits) * 15)
    return score, hits
