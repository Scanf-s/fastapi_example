from passlib.context import CryptContext


class UserDependencies:
    def __init__(self):
        self._user_service_instance = None
        self._auth_service_instance = None
        self._password_context = CryptContext(schemes=["md5_crypt"], deprecated="auto")

    async def get_password_context(self) -> CryptContext:
        return self._password_context

    async def get_user_service(self):
        if self._user_service_instance is None:
            from user.services.user_services import UserService
            self._user_service_instance = UserService()
        return self._user_service_instance

    async def get_auth_service(self):
        if self._auth_service_instance is None:
            from user.services.auth_services import AuthService
            self._auth_service_instance = AuthService()
        return self._auth_service_instance

user_dependencies = UserDependencies()