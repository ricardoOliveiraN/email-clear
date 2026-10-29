from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.install import router as install_router
from app.api.v1.validate import router as validate_router
from app.api.v1.vote import router as vote_router

router = APIRouter()
router.include_router(health_router)
router.include_router(install_router)
router.include_router(validate_router)
router.include_router(vote_router)
