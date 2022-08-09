from fastapi import APIRouter
from models.innotter import Innotter
from database.crud import create_page, get_page
routes_stats = APIRouter()


@routes_stats.post("/create", response_model=Innotter)
def init(page: Innotter):
    return create_page(page.dict())


@routes_stats.get("/get/{user_id}/{page_id}")
def get_stats(user_id, page_id):
    return get_page(user_id=user_id, page_id=page_id)
