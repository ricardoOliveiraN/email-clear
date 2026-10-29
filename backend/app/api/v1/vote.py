from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_install
from app.db.session import get_session
from app.domain.normalize import normalize_sender
from app.domain.score import sender_status
from app.models.instalacao import Instalacao
from app.models.voto_remetente import VotoRemetente
from app.schemas.vote import VoteRequest, VoteResponse
from app.services.remetentes import get_or_create_remetente

router = APIRouter()


@router.post("/vote", response_model=VoteResponse, tags=["community"])
async def vote(
    payload: VoteRequest,
    instalacao: Annotated[Instalacao, Depends(require_install)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> VoteResponse:
    """Registra/atualiza o voto da instalação sobre um remetente (ADR-0008).

    1 voto por instalação por remetente (dedup via UNIQUE). Voto pode ser trocado.
    """
    endereco = normalize_sender(payload.sender)
    if not endereco:
        raise HTTPException(status_code=400, detail="remetente inválido")

    remetente = await get_or_create_remetente(session, endereco)

    result = await session.execute(
        select(VotoRemetente).where(
            VotoRemetente.instalacao_id == instalacao.id,
            VotoRemetente.remetente_id == remetente.id,
        )
    )
    voto = result.scalar_one_or_none()

    if voto is None:
        session.add(
            VotoRemetente(
                instalacao_id=instalacao.id,
                remetente_id=remetente.id,
                valor=payload.valor,
            )
        )
        if payload.valor == "dangerous":
            remetente.votos_perigosos += 1
        remetente.votos_totais += 1
    elif voto.valor != payload.valor:
        if payload.valor == "dangerous":
            remetente.votos_perigosos += 1
        else:
            remetente.votos_perigosos -= 1
        voto.valor = payload.valor
    # mesmo valor → idempotente

    await session.commit()

    votos_seguros = remetente.votos_totais - remetente.votos_perigosos
    status, _ = sender_status(remetente.votos_perigosos, remetente.votos_totais)

    return VoteResponse(
        sender=endereco,
        status=status,
        votos_perigosos=remetente.votos_perigosos,
        votos_seguros=votos_seguros,
        votos_totais=remetente.votos_totais,
    )
