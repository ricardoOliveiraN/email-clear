from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Link(Base, TimestampMixin):
    """Link normalizado, com reputação agregada (ADR-0007)."""

    __tablename__ = "link"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # URL canônica (normalizada)
    url_normalizada: Mapped[str] = mapped_column(String(2048), nullable=False, unique=True, index=True)
    dominio: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    # unknown | safe | dangerous
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="unknown", server_default="unknown"
    )
