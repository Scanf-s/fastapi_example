from pydantic import BaseModel


class SignUpDTO(BaseModel):
    email: str
    password: str
