from fastapi import APIRouter, Depends, Header, Response, status

from server.db.cache import Cache
from server.exceptions import KeyNotFound
from server.schemas import EncryptionMessage
from server.tools import rc4
from server.tools.example_message import MESSAGE


api = APIRouter(tags=["RC4"], prefix="/encryption")


async def get_key(User: str = Header(...)):
    key = await Cache().get(User)
    if not key:
        raise KeyNotFound
    return key


@api.post(
    "/message",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
)
async def handle_external_message(message: EncryptionMessage, key: str = Depends(get_key)):
    print("Принял зашифрованное сообщение:", message.text, sep="\n", end="\n\n")
    decrypted_message = rc4(message.text, key)
    print("Расшифровка сообщения:", decrypted_message, sep="\n", end="\n\n")


@api.get(
    "/message",
    status_code=status.HTTP_200_OK,
    response_model=EncryptionMessage,
)
async def handle_internal_message(key: str = Depends(get_key)):
    encrypted_message = rc4(MESSAGE, key)
    print("Отправил сообщение:", encrypted_message, sep="\n", end="\n\n")
    return EncryptionMessage(text=encrypted_message)
