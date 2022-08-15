from fastapi import APIRouter
from models.innotter import Innotter
from database.crud import CRUDManager

router_innotter = APIRouter()


@router_innotter.get("/get/{user_id}/{page_id}")
def get_stats(user_id, page_id):
    """Temporary Template"""
    return CRUDManager.get_stats(user_id=user_id, page_id=page_id)
