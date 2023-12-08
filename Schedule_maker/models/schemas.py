from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserScheme(BaseModel):
    username: str
    email: str | None = None
    is_verified: bool | None = None

