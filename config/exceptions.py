from fastapi import FastAPI, Request
import jwt
from fastapi.responses import JSONResponse

class ObjectNotFound(Exception):
    pass

class UserAlreadyExists(Exception):
    pass

def register_exception_handlers(app: FastAPI):
    # 예외 핸들러 등록
    @app.exception_handler(jwt.exceptions.ExpiredSignatureError)
    @app.exception_handler(jwt.exceptions.InvalidTokenError)
    async def token_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid Token", "error_message": str(exc)}
        )

    @app.exception_handler(ObjectNotFound)
    async def object_not_found_handler(request: Request, exc: ObjectNotFound):
        return JSONResponse(
            status_code=404,
            content={"error": "ObjectNotFound", "error_message": str(exc)}
        )

    @app.exception_handler(UserAlreadyExists)
    async def user_exists_handler(request: Request, exc: UserAlreadyExists):
        return JSONResponse(
            status_code=400,
            content={"error": "UserAlreadyExists", "error_message": str(exc)}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"error": "InternalServerError", "error_message": str(exc)}
        )