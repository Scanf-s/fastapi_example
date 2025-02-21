from pydantic import BaseModel

class ValidateTokenRequestBody(BaseModel):
    token: str
