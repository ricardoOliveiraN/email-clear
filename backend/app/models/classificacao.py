from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, Numeric, String, func, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Classificacao(Base):
    """Resultado de classificação, chaveado por hash de conteúdo (cache L2 — ADR-0015)."""

    __tablename__ = "classificacao"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # sha256(sender+subject+body normalizados)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    score: Mapped[int] = mapped_column(Integer, nullable=False)
    # safe | suspicious | dangerous | unknown
    nivel: Mapped[str] = mapped_column(String(16), nullable=False)

    # sinais disparados e explicação (transparência — ADR-0007)
    sinais: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict, server_default=text("'{}'::jsonb")
    )
    explicacao: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict, server_default=text("'{}'::jsonb")
    )

    # llm | heuristica | cache
    origem: Mapped[str] = mapped_column(String(16), nullable=False)
    modelo_ia: Mapped[str | None] = mapped_column(String(64), nullable=True)
    custo_usd: Mapped[float | None] = mapped_column(Numeric(10, 6), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    # TTL do cache L2 (ADR-0015)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
