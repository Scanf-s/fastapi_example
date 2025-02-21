from fastapi.routing import APIRouter

router = APIRouter(
    prefix="/auth"
)

@router.post("/login")
async def login():
    pass

@router.post("/logout")
async def logout():
    pass