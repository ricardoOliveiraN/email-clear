import hashlib
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import check_install_rate_limit
from app.core.config import get_settings
from app.core.security import hash_install_id, new_install_id, sign_install_id
from app.db.session import get_session
from app.models.instalacao import Instalacao
from app.schemas.install import InstallResponse

router = APIRouter()


@router.post("/install", response_model=InstallResponse, tags=["identity"])
async def install(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> InstallResponse:
    """Emite identidade de instalação anônima (ADR-0014): install_id + token HMAC."""
    settings = get_settings()
    client_ip = request.client.host if request.client else "unknown"
    check_install_rate_limit(client_ip)

    install_id = new_install_id()
    token = sign_install_id(install_id, settings.install_token_secret)

    session.add(
        Instalacao(
            id=hash_install_id(install_id),
            token_hash=hashlib.sha256(token.encode("utf-8")).hexdigest(),
        )
    )
    await session.commit()

    return InstallResponse(install_id=install_id, token=token)
