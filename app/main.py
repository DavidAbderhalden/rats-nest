"""Core module of the application used to initialize it"""
from typing import Any

from fastapi import FastAPI, Request

from app.utils import AppExceptionHandler
from app.controller.v1 import api_controller

app = FastAPI()


@app.get('/favicon.ico')
async def get_favicon() -> Any:
    return 'ok'


@app.exception_handler(AppExceptionHandler)
async def app_exception_handler(request: Request) -> Any:
    return await AppExceptionHandler.handle_exception_case(request)


@app.on_event('startup')
def app_init() -> None:
    pass


app.include_router(api_controller)
