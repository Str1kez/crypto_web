function fastBinPow(number, exp, mod) {
    let result = 1
    while (exp !== 0) {
        if (exp & (1 === 1)) result = (result * number) % mod
        exp >>>= 1
        number = (number * number) % mod
    }
    return result
}

function getRandomArbitrary(min, max) {
    return Math.floor(Math.random() * (max - min)) + min
}

// ! Не нужны

function euclideanAlgorithm(a, b) {
    let temp
    if (a < b)
        // a, (b = b), a
        while (a % b) {
            temp = b
            b = a % b
            a = temp
        }
    return b
}

function millerRabin(num, rounds = 5) {
    if (num == 2) return true
    if (num % 2 == 0) return false

    let t = num - 1
    let s = 0
    while (t % 2 == 0) {
        t = Math.floor(t / 2)
        s++
    }
    for (let i = 0; i < rounds; i++) {
        let a = getRandomArbitrary(2, num - 1)
        let x = fastBinPow(a, t, num)
        if (x === 1 || x === num - 1) continue
        for (let j = 0; j < s - 1; j++) {
            x = fastBinPow(x, 2, num)
            if (x === 1) return false
            if (x === num - 1) break
            if (j === s - 2) return false
        }
    }
    return true
}
