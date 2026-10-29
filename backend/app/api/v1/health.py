from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import async_session

router = APIRouter()


@router.get("/healthz", tags=["health"])
async def healthz() -> dict[str, str]:
    """Liveness/readiness básica: processo + alcance do PostgreSQL."""
    try:
        async with async_session() as session:
            await session.execute(text("SELECT 1"))
        database = "ok"
    except Exception:  # noqa: BLE001 — degradação silenciosa, sem expor detalhes
        database = "error"

    return {
        "status": "ok" if database == "ok" else "degraded",
        "database": database,
    }
