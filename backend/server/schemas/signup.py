from typing import Self

from fastapi import Form
from pydantic import BaseModel


class SignUpRequest(BaseModel):
    username: str
    password: str

    @classmethod
    def as_form(
        cls,
        username: str = Form(..., min_length=5, max_length=30),
        password: str = Form(..., min_length=8, max_length=32),
    ) -> Self:
        return cls(username=username, password=password)
