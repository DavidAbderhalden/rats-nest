from fastapi import FastAPI, Request
from app.libs.utils.app_exception_handler import AppExceptionHandler
from app.libs.controller.app_controller import appController
from app.libs.services.database_operations import databaseOperationsService
from app.libs.models.database_models import TestModel
from typing import Any

app = FastAPI()

@app.get('/favicon.ico')
async def get_favicon() -> Any:
    return 'ok'

@app.exception_handler(AppExceptionHandler)
async def app_exception_handler(request: Request) -> Any:
    return await AppExceptionHandler.handle_exception_case(request)

@app.on_event('startup')
def app_init() -> None:
    with databaseOperationsService.session() as sess:
        test: TestModel = TestModel()
        sess.add(test)

app.include_router(appController)