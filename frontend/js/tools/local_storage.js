export function getUserWithKey() {
    const user = localStorage.getItem('username')
    const key = localStorage.getItem(user)
    if (user == null || key == null) {
        throw new Error(JSON.stringify({ message: 'no keys in localStorage' }))
    }
    return { user, key }
}
