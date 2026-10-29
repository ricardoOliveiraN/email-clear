"""Extração e normalização de links do conteúdo do e-mail."""

from app.domain.normalize import extract_urls, normalize_url


def extract_and_normalize_urls(body: str | None, subject: str | None = None) -> list[str]:
    raw = extract_urls(body) + extract_urls(subject)
    seen: set[str] = set()
    result: list[str] = []
    for url in raw:
        normalized = normalize_url(url)
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result
