from server.exceptions import InvalidSignature
from server.tools.diffie_hellman import fast_bin_pow
from server.tools.hash import get_hash


def signature_verify(message: str, key: int, n: int, signature: list[str]):
    internal_hash = get_hash(message)
    computed_signature = "".join(chr(fast_bin_pow(int(c), key, n)) for c in signature)
    if internal_hash != computed_signature:
        raise InvalidSignature
