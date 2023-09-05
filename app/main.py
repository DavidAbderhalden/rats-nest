"""Core module of the application used to initialize it"""
from typing import Any

from fastapi import FastAPI

from app.controller.v1 import api_controller

app = FastAPI()


@app.get('/favicon.ico')
async def get_favicon() -> Any:
    return 'ok'


@app.on_event('startup')
def app_init() -> None:
    pass


app.include_router(api_controller)
