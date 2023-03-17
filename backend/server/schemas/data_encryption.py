from pydantic import BaseModel


class EncryptionMessage(BaseModel):
    text: str
    exposed_key: str
    n: str
    signature: list[str]
