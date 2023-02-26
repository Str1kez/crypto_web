const web3 = window.Web3
const signin_url = 'http://localhost:8001/api/v1/auth/signin'
const code_url = 'http://localhost:8001/api/v1/auth/code'
const exchange_request_url = 'http://localhost:8001/api/v1/key/request'
const exchange_perform_url = 'http://localhost:8001/api/v1/key/exchange'
const bitLength = 128

function fastBinPow(number, exp, mod) {
    let result = 1n
    while (exp !== 0n) {
        if (exp % 2n === 1n) result = (result * number) % mod
        exp /= 2n
        number = (number * number) % mod
    }
    return result
}

function getRandomArbitrary(min, max) {
    return Math.floor(Math.random() * (max - min)) + min
}

function performPassword(password, codeHash) {
    const passwordHash = web3.utils.sha3(password)
    const combinedHash = web3.utils.sha3(passwordHash + codeHash)
    return combinedHash
}

async function get_code(formData) {
    return fetch(code_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: formData.get('username') }),
    })
        .then((response) => response.json())
        .then((json) => {
            if (json.code != undefined) {
                return json.code
            }
            throw new Error(JSON.stringify(json))
        })
}

async function signin(formData, code, success_field) {
    const request = await fetch(signin_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: formData.get('username'),
            password_hash: performPassword(formData.get('password'), code),
        }),
    })
    if (request.ok && request.status == 202) {
        success_field.hidden = false
        success_field.innerHTML = `Hello, ${formData.get(
            'username'
        )}! <br /> You are logged in!`
        return formData.get('username')
    }
    const json = await request.json()
    throw new Error(JSON.stringify(json))
}

async function get_exchange_params(username) {
    const request = await fetch(exchange_request_url + `/${bitLength}`, {
        method: 'GET',
        headers: {
            User: username,
        },
    })
    const json = await request.json()
    if (request.ok && request.status === 202) {
        return { ...json, username: username }
    }
    throw new Error(JSON.stringify(json))
}

async function generate_key(data) {
    const b = BigInt(getRandomArbitrary(10000, 100000))
    const B = fastBinPow(BigInt(data.g), b, BigInt(data.p))
    const request = await fetch(exchange_perform_url + `/${B}`, {
        method: 'POST',
        headers: {
            User: data.username,
        },
    })
    if (request.ok && request.status === 201) {
        console.log(`b=${b}\nB=${B}`)
        console.log(data)
        const key = fastBinPow(BigInt(data.A), b, BigInt(data.p))
        console.log(`key = ${key}`)
        return
    }
    const json = await request.json()
    throw new Error(JSON.stringify(json))
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

const form = document.forms.signin
form.addEventListener(
    'submit',
    (event) => {
        const error_output = document.querySelector('#error')
        const success_output = document.querySelector('#success')
        const formData = new FormData(form)

        get_code(formData)
            .finally(() => {
                error_output.hidden = true
            })
            .then((code) => signin(formData, code, success_output))
            .then((username) => get_exchange_params(username))
            .then((data) => generate_key(data))
            .catch((error) => errorHandler(error, error_output, success_output))

        event.preventDefault()
    },
    false
)
