from typing import Literal

from pydantic import BaseModel


class VoteRequest(BaseModel):
    sender: str
    valor: Literal["dangerous", "safe"]


class VoteResponse(BaseModel):
    sender: str
    status: str  # dangerous | legitimate | unknown
    votos_perigosos: int
    votos_seguros: int
    votos_totais: int
