import random

from server.tools.diffie_hellman import miller_rabin


def euler_function(p: int, q: int) -> int:
    return (p - 1) * (q - 1)


def extended_euclidean_algorithm(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    gcd, s, t = extended_euclidean_algorithm(b, a % b)
    return gcd, t, s - t * (a // b)


def get_prime(bit_len: int) -> int:
    x = random.randint(2 ** (bit_len - 1), 2**bit_len)
    while not miller_rabin(x):
        x = random.randint(2 ** (bit_len - 1), 2**bit_len)
    return x


def get_public_key(euler: int) -> int:
    key_len = 10 ** (len(str(euler)) // 3)
    key = random.randint(key_len, 10 * key_len)
    while extended_euclidean_algorithm(key, euler)[0] != 1:
        key = random.randint(key_len, 10 * key_len)
    return key


def get_private_key(euler: int, public_key: int) -> int:
    return extended_euclidean_algorithm(public_key, euler)[1] % euler
