import Axios from 'axios';

import { getUserToken } from './authUtils.js';

const { VITE_API_URL: API_URL } = import.meta.env;

export function publicApi(headers) {
    return Axios.create({
        baseURL: API_URL,
        timeout: 40000,
        headers: { ...headers },
    });
}

export function privateApi(headers) {
    const token = getUserToken();
    return Axios.create({
        baseURL: API_URL,
        timeout: 40000,
        headers: { ...headers, Authorization: `Bearer ${token}` },
    });
}
