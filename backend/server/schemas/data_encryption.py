from pydantic import BaseModel


class EncryptionMessage(BaseModel):
    text: str
