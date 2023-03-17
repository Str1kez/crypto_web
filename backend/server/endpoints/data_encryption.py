from fastapi import APIRouter, Depends, Header, Response, status

from server.db.cache import Cache
from server.exceptions import KeyNotFound
from server.schemas import EncryptionMessage
from server.tools import rc4
from server.tools.diffie_hellman import fast_bin_pow
from server.tools.example_message import MESSAGE
from server.tools.hash import get_hash
from server.usecase.digital_signature import signature_verify


api = APIRouter(tags=["RC4"], prefix="/encryption")


async def get_key(User: str = Header(...)):
    key = await Cache().get(User)
    if not key:
        raise KeyNotFound
    return key


async def get_rsa_params() -> tuple[int, int, int]:
    public_key = await Cache().get("public_rsa")
    private_key = await Cache().get("private_rsa")
    n = await Cache().get("n")
    return int(public_key), int(private_key), int(n)


@api.post(
    "/message",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
)
async def handle_external_message(message: EncryptionMessage, key: str = Depends(get_key)):
    print(
        "Принял зашифрованное сообщение:",
        message.text,
        "Открытый ключ клиента:",
        message.exposed_key,
        "ЭЦП:",
        message.signature,
        sep="\n",
        end="\n\n",
    )
    decrypted_message = rc4(message.text, key)
    print("Расшифровка сообщения:", decrypted_message, sep="\n", end="\n\n")
    print(message.signature[0], message.exposed_key, message.n)
    # signature_verify(decrypted_message, int(message.exposed_key), int(message.n), message.signature)
    # print("Подлинность подтверждена!", end="\n\n")


@api.get(
    "/message",
    status_code=status.HTTP_200_OK,
    response_model=EncryptionMessage,
)
async def handle_internal_message(key: str = Depends(get_key)):
    encrypted_message = rc4(MESSAGE, key)
    public_key, private_key, n = await get_rsa_params()
    message_signature = [str(fast_bin_pow(ord(c), private_key, n)) for c in get_hash(MESSAGE)]

    print(
        "Отправил сообщение:",
        encrypted_message,
        "Открытый ключ для расшифровки:",
        public_key,
        "n:",
        n,
        "Hash текста:",
        get_hash(MESSAGE),
        sep="\n",
        end="\n\n",
    )
    return EncryptionMessage(text=encrypted_message, exposed_key=str(public_key), n=str(n), signature=message_signature)
