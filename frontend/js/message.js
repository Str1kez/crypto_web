const url = 'http://localhost:8001/api/v1/encryption/message'
const chatButton = document.getElementById('chat_button')
const chatText = document.getElementById('textarea_chat')
const chatSuccess = document.getElementById('success_chat')
const chatError = document.getElementById('error_chat')

const messageSuccess = document.getElementById('success_message')
const messageError = document.getElementById('error_message')
const messageButton = document.getElementById('message_button')
const messageText = document.getElementById('textarea_message')

chatButton.onclick = async () => {
    const user = localStorage.getItem('username')
    const key = localStorage.getItem(user)
    if (user == null || key == null) {
        errorHandler(new Error(JSON.stringify({ message: 'no keys in localStorage' })), chatError, chatSuccess)
        return
    }
    const encryptedMessage = rc4(chatText.value, key)
    const request = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            User: user,
        },
        body: JSON.stringify({ text: encryptedMessage }),
    })
    if (request.ok && request.status === 201) {
        console.log(`Улетело зашифрованное сообщение:\n${encryptedMessage}`)
        chatError.hidden = true
        chatSuccess.hidden = false
        chatSuccess.innerHTML = 'Сообщение отправлено!'
        return
    }
    const json = await request.json()
    errorHandler(new Error(JSON.stringify(json)), chatError, chatSuccess)
}

messageButton.onclick = async () => {
    // TODO: GET data form bakend, show up encrypted message and decrypted paste in messageText.value
}

function errorHandler(error, err, success) {
    data = JSON.parse(error.message)
    err.hidden = false
    success.hidden = true
    if (data.message != undefined) {
        err.innerHTML = data.message
        return
    }
    let errors = ''
    console.log(data)
    for (let x of data['detail']) {
        errors += x.loc.pop() + ': ' + x.msg + ' <br />'
    }
    err.innerHTML = errors
}

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

    i = 0
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
