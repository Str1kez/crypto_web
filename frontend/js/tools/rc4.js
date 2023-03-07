function rc4(data, key) {
    let s = [],
        j = 0,
        x,
        result = ''

    for (let i = 0; i < 256; i++) {
        s[i] = i
    }

    for (let i = 0; i < 256; i++) {
        j = (j + s[i] + key.charCodeAt(i % key.length)) % 256
        x = s[i]
        s[i] = s[j]
        s[j] = x
    }

    let i = 0
    j = 0

    for (let y = 0; y < data.length; y++) {
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        x = s[i]
        s[i] = s[j]
        s[j] = x
        result += String.fromCharCode(data.charCodeAt(y) ^ s[(s[i] + s[j]) % 256])
    }

    return result
}

export { rc4 }
