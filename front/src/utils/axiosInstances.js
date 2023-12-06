import Axios from 'axios';
import { getUserToken } from '/src/utils/authUtils.js';

const BASE_PATH = 'http://localhost:5000/v1';

export function publicApi(headers) {
    return Axios.create({
        baseURL: BASE_PATH,
        timeout: 40000,
        headers: { ...headers },
    });
}

export function privateApi(headers) {
    console.log('Getting token from local storage.');
    const token = getUserToken();
    console.log(token);
    return Axios.create({
        baseURL: BASE_PATH,
        timeout: 40000,
        headers: { ...headers, Authorization: `Bearer ${token}` },
    });
}
