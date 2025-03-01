from fastapi.routing import APIRouter
from fastapi import Depends
from typing import Annotated
from sqlmodel import Session


from user.models import User
from user.schemas.signup import SignUp
from user.services.user_services import UserService
from config.dependencies import get_database_session
from user.dependencies import user_dependencies, UserDependencies
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from fastapi import status


router = APIRouter(
    prefix="/user"
)

@router.post("")
async def signup(
        register_data: SignUp,
        password_context: CryptContext = Depends(user_dependencies.get_password_context),
        user_service: UserService = Depends(user_dependencies.get_user_service),
        database_session: Session = Depends(get_database_session)
):
    user: User = await user_service.create_user(
        register_data=register_data.model_dump(),
        password_context=password_context,
        database_session=database_session
    )
    return JSONResponse(
        content=user.model_dump(), # TODO: 추후 반환할 정보 수정 예정
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
