from fastapi import FastAPI, HTTPException
import asyncio
from core.consumer import PikaClient
from core.urls import router
from database.db import create_tables
from database.crud import CRUDManager


class Statistic(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.handle_incoming_messages)

    @classmethod
    def handle_incoming_messages(cls, body, method):
        print(method, body, sep="\n")
        match method:
            case "page created":
                CRUDManager.create_page(body)
            case "add followers" | "remove followers" | "new post" | "like":
                CRUDManager.update_param(method, body)
            case "page deleted":
                CRUDManager.delete_page(body)
            case _:
                raise HTTPException(status_code=500)


app = Statistic()
app.include_router(router)

create_tables()


@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task
