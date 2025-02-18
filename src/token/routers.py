from fastapi.routing import APIRouter
from src.token.schemas.token_refresh_dto import TokenRefreshDTO

router = APIRouter(
    prefix="/token"
)

@router.get("")
async def test_token() -> TokenRefreshDTO:
    return TokenRefreshDTO(access_token="test", refresh_token="test")

@router.get("/refresh")
async def refresh_token() -> TokenRefreshDTO:
    return TokenRefreshDTO(access_token="test", refresh_token="test")