from pydantic import BaseModel


class KeyExchangeResponse(BaseModel):
    g: str
    A: str
    p: str
