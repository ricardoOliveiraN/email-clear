"""Normalização e derivação de chaves (remetente, URL, hash de conteúdo)."""

import hashlib
import re
from urllib.parse import urlsplit, urlunsplit

_WS = re.compile(r"\s+")
_URL_RE = re.compile(r"https?://[^\s<>\"')\]]+", re.IGNORECASE)


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    return _WS.sub(" ", value).strip().lower()


def normalize_sender(sender: str | None) -> str:
    return normalize_text(sender)


def extract_domain(address: str | None) -> str:
    """Extrai o domínio de um endereço (ou devolve o próprio valor se não houver '@')."""
    if not address:
        return ""
    address = normalize_text(address)
    if "@" in address:
        address = address.rsplit("@", 1)[1]
    return address.strip()


def normalize_url(url: str) -> str:
    """Canonicaliza uma URL para deduplicação (esquema/host lowercase, porta default removida, sem fragmento)."""
    url = url.strip()
    if not url:
        return ""
    try:
        parts = urlsplit(url)
        scheme = parts.scheme.lower() or "http"
        host = (parts.hostname or "").lower().rstrip(".")
        if not host:
            return url.lower()
        if parts.port and not (
            (scheme == "http" and parts.port == 80)
            or (scheme == "https" and parts.port == 443)
        ):
            netloc = f"{host}:{parts.port}"
        else:
            netloc = host
        path = parts.path or "/"
        return urlunsplit((scheme, netloc, path, parts.query, ""))
    except ValueError:
        return url.lower()


def content_hash(sender: str | None, subject: str | None, body: str | None) -> str:
    """SHA-256 da tupla normalizada (ADR-0015)."""
    raw = "\x00".join([normalize_text(sender), normalize_text(subject), normalize_text(body)])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def extract_urls(text: str | None) -> list[str]:
    if not text:
        return []
    return _URL_RE.findall(text)
