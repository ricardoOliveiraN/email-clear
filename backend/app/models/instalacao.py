from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Instalacao(Base):
    """Instalação anônima (ADR-0005/0014) — contabilidade best-effort, sem PII."""

    __tablename__ = "instalacao"

    # sha256(install_id) — privacidade (ADR-0005 §6)
    id: Mapped[str] = mapped_column(String(64), primary_key=True)

    # hash do token emitido, para rotação/revogação
    token_hash: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # quota best-effort (não é autorização)
    requests_total: Mapped[int] = mapped_column(
        BigInteger, nullable=False, default=0, server_default="0"
    )
    requests_today: Mapped[int] = mapped_column(
        BigInteger, nullable=False, default=0, server_default="0"
    )
    day_key: Mapped[str] = mapped_column(
        String(10), nullable=False, default="", server_default=""
    )
