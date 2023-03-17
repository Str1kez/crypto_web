import { fastBinPow, getBigRandomArbitrary } from './diffie_hellman.js'

function euler_function(p, q) {
    return (p - 1n) * (q - 1n)
}

function miller_rabin(num, rounds = 5n) {
    if (num == 2n) return true
    if (num % 2n == 0n) return false

    let t = num - 1n
    let s = 0n
    while (t % 2n == 0n) {
        t /= 2n
        s++
    }
    for (let i = 0n; i < rounds; i++) {
        let a = getBigRandomArbitrary(2n, num - 1n)
        let x = fastBinPow(a, t, num)
        if (x === 1n || x === num - 1n) continue
        for (let j = 0n; j < s - 1n; j++) {
            x = fastBinPow(x, 2n, num)
            if (x === 1n) return false
            if (x === num - 1n) break
            if (j === s - 2n) return false
        }
    }
    return true
}

function extended_euclidean_algorithm(a, b) {
    if (b == 0n) return [a, 1n, 0n]
    let [gcd, s, t] = extended_euclidean_algorithm(b, a % b)

    return [gcd, t, s - t * (a / b)]
}

function get_prime(bit_len) {
    let x = getBigRandomArbitrary(2n ** (bit_len - 1n), 2n ** bit_len)
    while (!miller_rabin(x, bit_len)) {
        x = getBigRandomArbitrary(2n ** (bit_len - 1n), 2n ** bit_len)
    }
    return x
}

function get_public_key(euler) {
    const key_len = 10n ** BigInt(Math.floor(euler.toString().length / 3))
    let key = getBigRandomArbitrary(key_len, 10n * key_len)
    while (extended_euclidean_algorithm(key, euler)[0] != 1n) {
        key = getBigRandomArbitrary(key_len, 10n * key_len)
    }
    return key
}

function get_private_key(euler, public_key) {
    return extended_euclidean_algorithm(public_key, euler)[1] % euler
}

export { get_private_key, get_public_key, get_prime, euler_function }
