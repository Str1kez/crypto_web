from hashlib import sha1

from server.config.settings import DefaultSettings


def __paste_salt(password: str) -> str:
    result = []
    for p, s in zip(password, DefaultSettings().PASSWORD_SALT):
        result.append(p + s)
    return "".join(result)


def password_hash(password: str) -> str:
    salty_password = __paste_salt(password)
    hash_obj = sha1(str.encode(salty_password))
    return hash_obj.hexdigest()
