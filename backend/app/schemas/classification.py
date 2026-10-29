from pydantic import BaseModel, Field


class EmailPayload(BaseModel):
    """Payload de validação recebido da extensão (alinhado a `OpenedEmail`)."""

    sender: str | None = None
    subject: str | None = None
    body: str = ""


class Classification(BaseModel):
    """Resultado de classificação (alinhado a `Classification` da extensão)."""

    level: str  # safe | suspicious | dangerous | unknown
    score: int
    reasons: list[str] = Field(default_factory=list)

    # campos extras (superset — não quebram o contrato da extensão)
    sinais: dict = Field(default_factory=dict)
    origem: str = "heuristica"
    content_hash: str | None = None


class LookupRequest(BaseModel):
    content_hash: str


class LookupResponse(BaseModel):
    hit: bool
    classification: Classification | None = None
