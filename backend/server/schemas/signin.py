from pydantic import BaseModel, Field


class CodeRequest(BaseModel):
    username: str = Field(..., min_length=5, max_length=30)


class CodeResponse(BaseModel):
    code: str


class SignInRequest(BaseModel):
    username: str = Field(..., min_length=5, max_length=30)
    password_hash: str = Field(..., max_length=66, min_length=66)
