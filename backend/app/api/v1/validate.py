from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_install
from app.core.config import get_settings
from app.db.session import get_session
from app.domain.normalize import content_hash, normalize_sender
from app.domain.score import (
    CONTENT_MAX,
    combine_score,
    sender_is_dangerous,
    sender_is_legitimate,
    sender_status,
)
from app.models.classificacao import Classificacao
from app.models.instalacao import Instalacao
from app.schemas.classification import (
    Classification,
    EmailPayload,
    LookupRequest,
    LookupResponse,
)
from app.services.ai import get_content_analyzer
from app.services.links import extract_and_normalize_urls
from app.services.remetentes import get_or_create_remetente
from app.services.safebrowsing import get_link_checker

router = APIRouter()


def _to_classification(row: Classificacao) -> Classification:
    explicacao = row.explicacao or {}
    return Classification(
        level=row.nivel,
        score=row.score,
        reasons=list(explicacao.get("reasons", [])),
        sinais=row.sinais or {},
        origem=row.origem,
        content_hash=row.content_hash,
    )


async def _cached(session: AsyncSession, ch: str) -> Classificacao | None:
    now = datetime.now(UTC)
    result = await session.execute(
        select(Classificacao).where(Classificacao.content_hash == ch)
    )
    row = result.scalar_one_or_none()
    if row and (row.expires_at is None or row.expires_at > now):
        return row
    return None


@router.post("/validate/lookup", response_model=LookupResponse, tags=["validation"])
async def lookup(
    payload: LookupRequest,
    instalacao: Annotated[Instalacao, Depends(require_install)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> LookupResponse:
    """Pré-checagem por hash de conteúdo (ADR-0015): devolve cache se existir."""
    row = await _cached(session, payload.content_hash)
    if row is not None:
        return LookupResponse(hit=True, classification=_to_classification(row))
    return LookupResponse(hit=False, classification=None)


@router.post("/validate", response_model=Classification, tags=["validation"])
async def validate(
    payload: EmailPayload,
    instalacao: Annotated[Instalacao, Depends(require_install)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Classification:
    """Classificação completa: remetente (votos) → links (Safe Browsing) → conteúdo (IA)."""
    settings = get_settings()
    now = datetime.now(UTC)

    # quota best-effort (ADR-0005)
    today = now.date().isoformat()
    if instalacao.day_key != today:
        instalacao.day_key = today
        instalacao.requests_today = 0
    if instalacao.requests_today >= settings.validate_daily_quota:
        raise HTTPException(status_code=429, detail="quota diária excedida")
    instalacao.requests_today += 1
    instalacao.requests_total += 1
    instalacao.last_seen_at = now
    await session.commit()

    ch = content_hash(payload.sender, payload.subject, payload.body)

    # cache L2 por hash (ADR-0015)
    cached = await _cached(session, ch)
    if cached is not None:
        return _to_classification(cached)

    # 1. reputação do remetente (votos — ADR-0008)
    sender_votos_perigosos = 0
    sender_votos_totais = 0
    if normalize_sender(payload.sender):
        remetente = await get_or_create_remetente(session, payload.sender)
        sender_votos_perigosos = remetente.votos_perigosos
        sender_votos_totais = remetente.votos_totais

    # 2. links (Safe Browsing — ADR-0007)
    urls = extract_and_normalize_urls(payload.body, payload.subject)
    verdicts = await get_link_checker().check(urls) if urls else {}
    link_dangerous = any(v == "dangerous" for v in verdicts.values())

    # 3. conteúdo (IA ou heurística — ADR-0007)
    analysis = await get_content_analyzer().analyze(payload)

    # IA retorna 0–100; o componente de conteúdo vale 0–70 (ADR-0007).
    content_score = round(analysis.phishing_score * (CONTENT_MAX / 100))

    score, nivel = combine_score(
        content_score=content_score,
        sender_votos_perigosos=sender_votos_perigosos,
        sender_votos_totais=sender_votos_totais,
        link_dangerous=link_dangerous,
    )

    sender_status_value, _ = sender_status(sender_votos_perigosos, sender_votos_totais)

    reasons: list[str] = []
    if sender_is_dangerous(sender_votos_perigosos, sender_votos_totais):
        reasons.append("remetente marcado como perigoso pela comunidade")
    if sender_is_legitimate(sender_votos_perigosos, sender_votos_totais):
        reasons.append("remetente confiável (comunidade) — risco do conteúdo reduzido")
    if link_dangerous:
        reasons.append("link em lista de bloqueio")
    if analysis.indicators:
        reasons.append("indícios de phishing: " + ", ".join(analysis.indicators[:5]))
    if analysis.justification:
        reasons.append(analysis.justification)

    sinais = {
        "sender": {
            "status": sender_status_value,
            "votos_perigosos": sender_votos_perigosos,
            "votos_totais": sender_votos_totais,
        },
        "links": verdicts,
        "content": {
            "phishing_score": analysis.phishing_score,
            "indicators": analysis.indicators,
        },
    }

    origem = analysis.source

    session.add(
        Classificacao(
            content_hash=ch,
            score=score,
            nivel=nivel,
            sinais=sinais,
            explicacao={"reasons": reasons, "justification": analysis.justification},
            origem=origem,
            modelo_ia=settings.openrouter_model if analysis.source == "llm" else None,
            expires_at=now + timedelta(seconds=settings.cache_ttl_seconds),
        )
    )
    await session.commit()

    return Classification(
        level=nivel,
        score=score,
        reasons=reasons,
        sinais=sinais,
        origem=origem,
        content_hash=ch,
    )
