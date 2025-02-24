import uuid
from typing import Dict, Annotated

from fastapi.routing import APIRouter
from fastapi import status, Depends, Response, HTTPException
from fastapi.responses import JSONResponse

from jwt_token.models import TokenType
from jwt_token.schemas.token_refresh_dto import TokenRefreshDTO
from jwt_token.schemas.validate_token_request_body import ValidateTokenRequestBody
from jwt_token.services import TokenService

router = APIRouter(
    prefix="/token"
)

token_service_instance = TokenService()

def get_token_service() -> TokenService:
    return token_service_instance

@router.post("/refresh")
async def refresh(token_service: TokenService = Annotated[TokenService, Depends(get_token_service)]) -> JSONResponse:
    """
    만약 refresh token payload에 들어있는 사용자가 유효한 사용자라면,
    Refresh token을 사용하여 Access token 및 Refresh token 재발급 (Rotate)
    """
    user_id: uuid.UUID = uuid.uuid4() # TODO: 추후, middleware에서 검사 후 반환한 user_id를 사용해야함

    refresh_token: str = await token_service.create_token(user_id=user_id, token_type=TokenType.REFRESH)
    access_token: str = await token_service.create_token(user_id=user_id, token_type=TokenType.ACCESS)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content = TokenRefreshDTO(access_token=access_token, refresh_token=refresh_token).model_dump()
    )

@router.post("/validate")
async def validate_token(
        token_request: ValidateTokenRequestBody,
        token_service: TokenService = Annotated[TokenService, Depends(get_token_service)]
) -> Response:
    """
    토큰 유효성 검증 함수
    """
    token_dict: Dict = token_request.model_dump()
    is_valid: bool = await token_service.validate_token(token=token_dict.get("token"))
    if is_valid:
        return Response(status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
