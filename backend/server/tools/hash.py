# from hashlib import sha1

from web3 import Web3


# from server.config.settings import DefaultSettings


# def __paste_salt(password: str) -> str:
#     result = []
#     for p, s in zip(password, DefaultSettings().PASSWORD_SALT):
#         result.append(p + s)
#     return "".join(result)


def get_hash(data: str) -> str:
    # salty_password = __paste_salt(password)
    # password_in_bytes = str.encode(password)
    hash_obj = Web3.keccak(text=data)
    return hash_obj.hex()
