from fastapi import FastAPI
import asyncio
from core.consumer import PikaClient
from database.db import create_tables
from endpoints.innotter import routes_stats


class Statistic(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.handle_incoming_messages)

    @classmethod
    def handle_incoming_messages(cls, body):
        print("handle inc messages")


app = Statistic()

create_tables()

app.include_router(routes_stats, prefix="/innotter")

@app.on_event("startup")
async def startup():
    print("startup")
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task