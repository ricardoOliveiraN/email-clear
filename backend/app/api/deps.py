"""Dependências de segurança: rate-limit de emissão e autenticação por token."""

import time
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import hash_install_id, verify_install_token
from app.db.session import get_session
from app.models.instalacao import Instalacao

# Rate-limit em memória (por processo). Suficiente para dev/single-instance;
# produção exige store compartilhado (Redis) — ver ADR-0014.
_INSTALLS: dict[str, list[float]] = {}


def check_install_rate_limit(client_ip: str) -> None:
    settings = get_settings()
    now = time.time()
    window = settings.install_rate_limit_window_seconds
    bucket = [t for t in _INSTALLS.get(client_ip, []) if now - t < window]
    if len(bucket) >= settings.install_rate_limit_per_ip:
        raise HTTPException(status_code=429, detail="muitas instalações deste endereço")
    bucket.append(now)
    _INSTALLS[client_ip] = bucket


async def require_install(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Instalacao:
    """Valida o token de instalação (ADR-0014) e devolve a instalação correspondente."""
    settings = get_settings()
    token = request.headers.get("X-Install-Token")
    if not token:
        raise HTTPException(status_code=401, detail="token de instalação ausente")

    install_id = verify_install_token(token, settings.install_token_secret)
    if install_id is None:
        raise HTTPException(status_code=401, detail="token de instalação inválido")

    instalacao = await session.get(Instalacao, hash_install_id(install_id))
    if instalacao is None:
        raise HTTPException(status_code=401, detail="instalação desconhecida")

    return instalacao
