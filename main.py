from fastapi import FastAPI
from database.db import create_tables
from endpoints.innotter import routes_stats

app = FastAPI()

create_tables()

app.include_router(routes_stats, prefix="/innotter")
