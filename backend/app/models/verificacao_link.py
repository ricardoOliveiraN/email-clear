from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class VerificacaoLink(Base):
    """Histórico de verificação de um link por fonte (Safe Browsing / IA)."""

    __tablename__ = "verificacao_link"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    link_id: Mapped[int] = mapped_column(
        ForeignKey("link.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # safebrowsing | ia
    fonte: Mapped[str] = mapped_column(String(32), nullable=False)
    # safe | dangerous | unknown
    resultado: Mapped[str] = mapped_column(String(16), nullable=False)
    detalhe: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
