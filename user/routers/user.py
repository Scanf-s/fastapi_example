from fastapi.routing import APIRouter

router = APIRouter(
    prefix="/user"
)

@router.post("")
async def signup():
    pass

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
