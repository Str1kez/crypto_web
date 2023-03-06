import random

from fastapi import APIRouter, Header, Response, status
from fastapi.responses import JSONResponse
from pydantic import PositiveInt

from server.db.cache import Cache
from server.schemas.key_exchange import KeyExchangeResponse
from server.tools.diffie_hellman import fast_bin_pow, get_primitive_root, get_safe_prime


api = APIRouter(tags=["Keys"], prefix="/key")
TEMP_DB = {}


@api.get(
    "/request/{bit_len}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=KeyExchangeResponse,
)
async def dh_request(bit_len: PositiveInt, User: str = Header(...)):
    p = get_safe_prime(bit_len)
    g = get_primitive_root(bit_len, p)
    a = random.randint(10000, 100000)
    A = fast_bin_pow(g, a, p)
    print(f"Generated\n{p=}\n{g=}\n{a=}\n{A=}")
    TEMP_DB[User] = {"p": p, "g": g, "a": a, "A": A}
    return KeyExchangeResponse(g=str(g), p=str(p), A=str(A))


@api.post(
    "/exchange/{part_key}",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
)
async def key_generation(part_key: PositiveInt, User: str = Header(...)):
    if User not in TEMP_DB:
        return JSONResponse({"message": "your request not found"}, status.HTTP_404_NOT_FOUND)
    data = TEMP_DB[User]
    k = fast_bin_pow(part_key, data["a"], data["p"])
    await Cache().set(User, k)
    print(f"Key on server:\n{k=}")
