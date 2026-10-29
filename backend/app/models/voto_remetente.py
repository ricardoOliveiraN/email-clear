from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class VotoRemetente(Base):
    """Voto de uma instalação sobre um remetente (ADR-0008) — 1 voto por instalação."""

    __tablename__ = "voto_remetente"
    __table_args__ = (
        UniqueConstraint("instalacao_id", "remetente_id", name="uq_voto_instalacao_remetente"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    instalacao_id: Mapped[str] = mapped_column(
        ForeignKey("instalacao.id", ondelete="CASCADE"), nullable=False, index=True
    )
    remetente_id: Mapped[int] = mapped_column(
        ForeignKey("remetente.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # dangerous | safe
    valor: Mapped[str] = mapped_column(String(16), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
