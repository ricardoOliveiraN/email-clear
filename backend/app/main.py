from fastapi import FastAPI

from app.api.v1 import router as v1_router

app = FastAPI(
    title="email-clear",
    version="0.1.0",
    description="Validação de e-mails no Gmail: reputação de remetente, conteúdo (IA) e links.",
)

app.include_router(v1_router, prefix="/v1")


@app.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    return {"name": "email-clear", "docs": "/docs"}
