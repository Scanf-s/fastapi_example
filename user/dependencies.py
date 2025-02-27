from passlib.context import CryptContext
from user.services.user_services import UserService
from user.services.auth_services import AuthService


class UserDependencies:
    def __init__(self):
        self._user_service_instance = UserService()
        self._auth_service_instance = AuthService()
        self._password_context = CryptContext(schemes=["md5_crypt"], deprecated="auto")

    async def get_password_context(self) -> CryptContext:
        return self._password_context

    async def get_user_service(self) -> UserService:
        return self._user_service_instance

    async def get_auth_service(self) -> AuthService:
        return self._auth_service_instance

user_dependencies = UserDependencies()