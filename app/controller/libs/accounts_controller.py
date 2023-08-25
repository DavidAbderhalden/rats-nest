from fastapi import APIRouter, HTTPException

from app.schemas import PostAccountsRegisterSchema
from app.services import databaseOperationsService

accountsController: APIRouter = APIRouter(prefix='/accounts')


@accountsController.post('/register')
async def register(body: PostAccountsRegisterSchema):
    if databaseOperationsService.create_customer(body):
        return {
            'name': 'success',
            'value': body
        }
    raise HTTPException(
        status_code=500,
        detail='Something went wrong during the creation of your account!'
    )

@accountsController.get('/username-availability/{username}')
async def username_availability(username: str):
    # TODO: Implement
    return {
        'username': username
    }