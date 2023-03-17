import { euler_function, get_prime, get_private_key, get_public_key } from './rsa.js'

export function getUserWithKey() {
    const user = localStorage.getItem('username')
    const key = localStorage.getItem(user)
    if (user == null || key == null) {
        throw new Error(JSON.stringify({ message: 'no keys in localStorage' }))
    }
    return { user, key }
}

export function generateRSAKeys() {
    const p = get_prime(16n)
    let q = get_prime(16n)
    while (q === p) {
        q = get_prime(16n)
    }
    const public_key = get_public_key(euler_function(p, q))
    const private_key = get_private_key(euler_function(p, q), public_key)
    console.log(p, q, euler_function(p, q))

    localStorage.setItem('n', (p * q).toString())
    localStorage.setItem('public_rsa', public_key.toString())
    localStorage.setItem('private_rsa', private_key.toString())
}
