from fastapi import APIRouter
from api.v1.urls import router_innotter

router_stats = APIRouter()

router_stats.include_router(router_innotter, prefix="/v1")
