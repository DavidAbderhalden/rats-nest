"""Core module of the application used to initialize it"""
import sys

from typing import Any

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.logger import logger

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.controller.v1 import api_controller
from app.repository import database_operations_service

app: FastAPI = FastAPI()
load_dotenv()


@app.get('/favicon.ico')
async def get_favicon() -> Any:
    return 'ok'


# FIXME: Logging context
@app.on_event('startup')
async def app_init() -> None:
    async with database_operations_service.session() as session:
        try:
            await session.execute(text('SELECT 1'))
            logger.info('INFO:     Connection to database established.')
        except SQLAlchemyError:
            logger.error("ERROR:    Couldn't connect to database!")
            sys.exit(0)


app.include_router(api_controller)
