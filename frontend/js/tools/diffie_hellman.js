function fastBinPow(number, exp, mod) {
    let result = 1n
    while (exp !== 0n) {
        if (exp % 2n === 1n) {
            result = (result * number) % mod
        }
        exp >>= 1n
        number = (number * number) % mod
    }
    return result
}

function getRandomArbitrary(min, max) {
    return Math.floor(Math.random() * (max - min)) + min
}

function getBigRandomArbitrary(lowBigInt, highBigInt) {
    if (lowBigInt >= highBigInt) {
        throw new Error('lowBigInt must be smaller than highBigInt')
    }

    const difference = highBigInt - lowBigInt
    const differenceLength = difference.toString().length
    let multiplier = ''
    while (multiplier.length < differenceLength) {
        multiplier += Math.random().toString().split('.')[1]
    }
    multiplier = multiplier.slice(0, differenceLength)
    const divisor = '1' + '0'.repeat(differenceLength)

    const randomDifference = (difference * BigInt(multiplier)) / BigInt(divisor)

    return lowBigInt + randomDifference
}

export { fastBinPow, getRandomArbitrary, getBigRandomArbitrary }
