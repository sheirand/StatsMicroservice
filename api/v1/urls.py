from fastapi import APIRouter, Depends
from core.authentication import JWTAuthentication
from models.innotter import Innotter
from database.crud import CRUDManager

router_innotter = APIRouter()


@router_innotter.get("/get/{page_id}")
def get_stats(page_id, user_id=Depends(JWTAuthentication())):
    """Temporary Template"""
    return CRUDManager.get_stats(user_id=str(user_id), page_id=page_id)
