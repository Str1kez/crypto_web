function errorHandler(error, err, success) {
    let data = JSON.parse(error.message)
    err.hidden = false
    success.hidden = true
    if (data.message != undefined) {
        err.innerHTML = data.message
        return
    }
    let errors = ''
    for (let x of data['detail']) {
        errors += x.loc.pop() + ': ' + x.msg + ' <br />'
    }
    err.innerHTML = errors
}

export { errorHandler }
