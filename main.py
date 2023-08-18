from fastapi import FastAPI, Request
from libs.utils.app_exception_handler import AppExceptionHandler
from libs.controller.app_controller import appController
from typing import Any

app = FastAPI()

@app.get('/favicon.ico')
async def get_favicon() -> Any:
    return 'ok'

@app.exception_handler(AppExceptionHandler)
async def app_exception_handler(request: Request) -> Any:
    return await AppExceptionHandler.handle_exception_case(request)

app.include_router(appController)