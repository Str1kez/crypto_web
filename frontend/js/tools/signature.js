import { fastBinPow } from './diffie_hellman.js'

export function getSignature(hash, key, n) {
    let temp = [...hash]
    return temp.map((item) => {
        return fastBinPow(BigInt(item.charCodeAt()), key, n).toString()
    })
}
