from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.normalize import extract_domain, normalize_sender
from app.models.remetente import Remetente


async def get_or_create_remetente(session: AsyncSession, sender: str) -> Remetente:
    """Busca (ou cria) o remetente normalizado pelo endereço."""
    endereco = normalize_sender(sender)
    dominio = extract_domain(endereco)

    result = await session.execute(select(Remetente).where(Remetente.endereco == endereco))
    remetente = result.scalar_one_or_none()
    if remetente is None:
        remetente = Remetente(endereco=endereco, dominio=dominio)
        session.add(remetente)
        await session.flush()
    return remetente
