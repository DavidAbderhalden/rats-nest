"""Core module of the application used to initialize it"""
from typing import Any

from fastapi import FastAPI, Request

from app.utils import AppExceptionHandler
from app.controller import appController
from app.services import databaseOperationsService
from app.models import CitiesModel, Countries

app = FastAPI()

@app.get('/favicon.ico')
async def get_favicon() -> Any:
    return 'ok'

@app.exception_handler(AppExceptionHandler)
async def app_exception_handler(request: Request) -> Any:
    return await AppExceptionHandler.handle_exception_case(request)

@app.on_event('startup')
def app_init() -> None:
    # pylint: disable=unused-variable
    with databaseOperationsService.session() as sess:
        # pylint: disable=unused-variable
        new_city: CitiesModel = CitiesModel(zip_code=5304, name='Endingen', country=Countries.CH)
        # sess.add(new_city)

app.include_router(appController)
