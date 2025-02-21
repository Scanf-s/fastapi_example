from fastapi.routing import APIRouter

router = APIRouter(
    prefix="/user"
)

@router.post("/")
async def signup():
    pass
