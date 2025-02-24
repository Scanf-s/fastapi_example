from fastapi.routing import APIRouter
from fastapi import Depends
from typing import Annotated
from user.schemas.sign_up_dto import SignUpDTO
from user.services.user_services import UserService
from fastapi.responses import JSONResponse
from fastapi import status


router = APIRouter(
    prefix="/user"
)

user_service_instance = UserService()
async def get_user_service() -> UserService:
    return user_service_instance

@router.post("")
async def signup(
        register_data: SignUpDTO,
        user_service: UserService = Annotated[UserService, Depends(get_user_service)]
):
    await user_service.create_user(register_data=register_data.model_dump())
    return JSONResponse(
        status_code=status.HTTP_201_CREATED
    )

@router.get("")
async def get_user():
    pass

@router.put("")
async def update_user():
    pass

@router.patch("")
async def partial_update_user():
    pass

@router.delete("")
async def delete_user():
    pass
