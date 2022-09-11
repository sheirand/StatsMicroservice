from fastapi import FastAPI
import asyncio
from core.consumer import PikaClient
from core.urls import router
from database.db import create_tables


class Statistic(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.handle_incoming_messages)

    @classmethod
    def handle_incoming_messages(cls, body, method):
        pass


app = Statistic()
app.include_router(router)

create_tables()


@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task
