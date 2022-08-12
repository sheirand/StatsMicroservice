from pydantic import BaseModel


class Stats(BaseModel):
    followers: int
    likes: int
    posts: int


class Innotter(BaseModel):
    user_id: str
    page_id: str
    statistic: Stats
