import { rc4 } from './tools/rc4.js'
import { errorHandler } from './error.js'
import { getUserWithKey } from './tools/local_storage.js'

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
    let data
    try {
        data = getUserWithKey()
    } catch (e) {
        errorHandler(e, chatError, chatSuccess)
        return
    }
    const { user, key } = data
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
    let data
    try {
        data = getUserWithKey()
    } catch (e) {
        errorHandler(e, messageError, messageSuccess)
        return
    }
    const { user, key } = data
    const request = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            User: user,
        },
    })
    const response = await request.json()
    if (request.ok && request.status === 200) {
        messageText.value = rc4(response.text, key)
        messageError.hidden = true
        messageSuccess.hidden = false
        messageSuccess.innerHTML = 'Сообщение получено!'
        console.log(`Получил сообщение от сервера:\n${response.text}`)
        return
    }
    errorHandler(new Error(JSON.stringify(response)), messageError, messageSuccess)
}
