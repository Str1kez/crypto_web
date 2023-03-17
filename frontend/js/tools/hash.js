const web3 = window.Web3

function getHash(data) {
    return web3.utils.sha3(data)
}

export { getHash }
