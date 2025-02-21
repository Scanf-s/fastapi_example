from fastapi.routing import APIRouter

router = APIRouter(
    prefix="/oauth"
)

@router.post("/google")
async def google_oauth():
    pass

@router.post("/kakao")
async def kakao_oauth():
    pass

@router.post("/naver")
async def naver_oauth():
    pass

@router.post("/twitter")
async def twitter_oauth():
    pass

@router.post("/github")
async def github_oauth():
    pass

@router.post("/apple")
async def apple_oauth():
    pass