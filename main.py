from fastapi import FastAPI, Request, Response
from libs.utils.app_exception_handler import AppExceptionHandler
from libs.controller.app_controller import appController

app = FastAPI()

@app.exception_handler(AppExceptionHandler)
async def app_exception_handler(request: Request) -> Response:
    return await AppExceptionHandler.handle_exception_case(request)

app.include_router(appController)