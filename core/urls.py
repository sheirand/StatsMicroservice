from fastapi import APIRouter
from api.urls import router_stats

router = APIRouter()

router.include_router(router_stats, prefix="/api")
