from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Remetente(Base, TimestampMixin):
    """Remetente normalizado, com contagens de votos desnormalizadas (ADR-0008)."""

    __tablename__ = "remetente"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # normalizado: lowercase + trim
    endereco: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    # domínio extraído e normalizado
    dominio: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    votos_perigosos: Mapped[int] = mapped_column(
        BigInteger, nullable=False, default=0, server_default="0"
    )
    votos_totais: Mapped[int] = mapped_column(
        BigInteger, nullable=False, default=0, server_default="0"
    )
