from fastapi import APIRouter
from .endpoints import api1, api2, api3

router = APIRouter()
router.include_router(api1.router, tags=["api1"])
router.include_router(api2.router, tags=["api2"])
router.include_router(api3.router, tags=["api3"])

