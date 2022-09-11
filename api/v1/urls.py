from fastapi import APIRouter, Depends
from core.authentication import JWTAuthentication
from models.innotter import Innotter
from pydantic.fields import List
from database.crud import CRUDManager


router_innotter = APIRouter()


@router_innotter.get("/get-stats", summary="Get statistic of user pages", response_model=List[Innotter])
def get_stats(user_id=Depends(JWTAuthentication())):
    return CRUDManager.get_stats(user_id=user_id)
