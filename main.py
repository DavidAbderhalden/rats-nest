from fastapi import FastAPI, Depends
from libs.services.database_operations import DatabaseOperationsService
from libs import deps

app = FastAPI()


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World!"}


@app.get("/hello/{name}")
async def say_hello(name: str) -> dict:
    return {"message": f"Hello {name}"}


@app.get("/test")
async def test(database_operations_service: DatabaseOperationsService = Depends(deps.get_database_operations_service)) -> dict:
    database_operations_service.add(1)
    counter: int = database_operations_service.get_counter()
    return {"counter": f"Counter is at {counter}"}