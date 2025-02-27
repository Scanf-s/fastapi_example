from fastapi.routing import APIRouter
from user.services.auth_services import auth_service_instance, AuthService
from user.schemas.login import LoginRequest
from fastapi import Depends
from typing import Annotated

router = APIRouter(
    prefix="/auth"
)

async def get_auth_service() -> AuthService:
    return auth_service_instance

@router.post("/login")
async def login(
    login_data: LoginRequest,
    auth_service: AuthService = Annotated[AuthService, Depends(get_auth_service)]
):
    await auth_service.login(email=login_data.email, password=login_data.password)
    return {
        "message": "Successfully logged in"
    }
    

@router.post("/logout")
async def logout():
    pass