import { fastBinPow } from './diffie_hellman.js'

export function getSignature(hash, key, n) {
    let temp = [...hash]
    return temp.map((item) => {
        return fastBinPow(BigInt(item.charCodeAt()), key, n).toString()
    })
}

export function verifySignature(hash, key, n, signature) {
    const calculatedHash = signature
        .map((item) => {
            return String.fromCharCode(Number(fastBinPow(BigInt(item), key, n)))
        })
        .join('')
    return hash === calculatedHash
}
