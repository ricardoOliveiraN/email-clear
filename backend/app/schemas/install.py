from pydantic import BaseModel


class InstallResponse(BaseModel):
    install_id: str
    token: str
