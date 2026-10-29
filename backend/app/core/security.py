"""Identidade de instalação anônima (ADR-0005/0014).

O token é `install_id + "." + HMAC-SHA256(segredo, install_id)`. O segredo vive
apenas no servidor; a extensão recebe o token e o reenvia em cada requisição.
"""

import hashlib
import hmac
import secrets

_TOKEN_SECRET = "install_token_secret"


def new_install_id() -> str:
    """Gera um install_id aleatório, sem PII (URL-safe)."""
    return secrets.token_urlsafe(24)


def _signature(install_id: str, secret: str) -> str:
    return hmac.new(secret.encode("utf-8"), install_id.encode("utf-8"), hashlib.sha256).hexdigest()


def sign_install_id(install_id: str, secret: str) -> str:
    """Assina um install_id, devolvendo o token completo `install_id.sig`."""
    return f"{install_id}.{_signature(install_id, secret)}"


def verify_install_token(token: str, secret: str) -> str | None:
    """Valida um token e devolve o install_id, ou `None` se inválido."""
    install_id, sep, _sig = token.rpartition(".")
    if not sep:
        return None
    expected = sign_install_id(install_id, secret)
    if not hmac.compare_digest(expected, token):
        return None
    return install_id


def hash_install_id(install_id: str) -> str:
    """Hash do install_id para armazenamento (privacidade — ADR-0005 §6)."""
    return hashlib.sha256(install_id.encode("utf-8")).hexdigest()
