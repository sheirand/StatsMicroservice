from fastapi import APIRouter
from models.innotter import Innotter
from database.crud import create_page, get_page

router_innotter = APIRouter()


@router_innotter.post("/create", response_model=Innotter)
def init(page: Innotter):
    """Temporary Template"""
    return create_page(page.dict())


@router_innotter.get("/get/{user_id}/{page_id}")
def get_stats(user_id, page_id):
    """Temporary Template"""
    return get_page(user_id=user_id, page_id=page_id)
