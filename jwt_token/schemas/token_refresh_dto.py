from pydantic import BaseModel


class TokenRefreshDTO(BaseModel):
    access_token: str
    refresh_token: str
