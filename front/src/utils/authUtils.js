export function getUserToken() {
    return localStorage.getItem('AUTH');
}

export function getAuthenticatedStatus() {
    const token = getUserToken();
    return !!token;
}

export function setUserToken(token) {
    localStorage.setItem('AUTH', token);
}

export function removeUserToken() {
    localStorage.removeItem('AUTH');
}
