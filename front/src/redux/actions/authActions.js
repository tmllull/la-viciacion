import { API_ENDPOINTS } from '../../constants/apiEndpoints.js';
import { privateApi } from '../../utils/axiosInstances.js';
import { getUserToken, setUserToken } from '../../utils/authUtils.js';

import { deleteAction, getAction, postAction } from './commonActions';

// COMENT ACTION TYPES
export const ACTIONS = {
    GET_AUTHENTICATED_USER: 'get_authenticated_user',
    LOGIN: 'login',
    SIGNUP: 'signup',
};

// export function fetchUserById(id, options, callbacks) {
//     return function (dispatch) {
//         const URL = USER_BY_ID.replace('{:id}', id);
//         getAction(ACTIONS.FETCH_USER_BY_ID, URL, null, dispatch, options, callbacks);
//     };
// }
//
// export function uploadAvatar(id, data, options, callbacks) {
//     return function (dispatch) {
//         const URL = UPLOAD_FILE.replace('{:id}', id);
//         const headers = {
//             'Content-Type': 'multipart/form-data',
//         };
//         postAction(ACTIONS.UPLOAD_AVATAR, URL, data, dispatch, options, callbacks, headers);
//     };
// }
//
// export function updateUserById(id, data, callbacks) {
//     return function (dispatch) {
//         const URL = UPDATE_PROFILE.replace('{:id}', id);
//         postAction(ACTIONS.UPDATE_PROFILE, URL, data, dispatch, {}, callbacks);
//     };
// }
//
// export function resetPasswordByEmail(email, callbacks) {
//     return function (dispatch) {
//         postAction(ACTIONS.RESET_PASSWORD, RESET_PASSWORD, { email }, dispatch, {}, callbacks);
//     };
// }
//
// export function deleteUser(data, callbacks) {
//     return function (dispatch) {
//         deleteAction(ACTIONS.DELETE_USER, DELETE_USER, data, dispatch, callbacks);
//     };
// }

export function getAuthenticatedUser(callbacks) {
    return function (dispatch) {
        getAction({
            type: ACTIONS.GET_AUTHENTICATED_USER,
            url: API_ENDPOINTS.AUTH.GET_AUTHENTICATED_USER,
            instance: privateApi,
            dispatch,
            callbacks,
        });
    };
}

export function login({ data, callbacks = {} }) {
    return function (dispatch) {
        function success(response) {
            console.log(response);
            console.log('Setting access token in local storage.');
            setUserToken(response.access_token);

            dispatch(getAuthenticatedUser(callbacks));
        }
        postAction({
            type: ACTIONS.LOGIN,
            url: API_ENDPOINTS.AUTH.LOGIN,
            dispatch,
            data,
            callbacks: { ...callbacks, success },
            headers: { 'content-type': 'application/x-www-form-urlencoded' },
        });
    };
}

export function signup({ data, callbacks = {} }) {
    return function (dispatch) {
        const {
            username,
            email,
            password,
            invitationKey,
        } = data
        function success() {
            dispatch(login({ data: { username, password }, callbacks }));
        }
        postAction({
            type: ACTIONS.SIGNUP,
            url: API_ENDPOINTS.AUTH.SIGNUP,
            dispatch,
            data: {
                username,
                email,
                password,
                invitation_key: invitationKey,
            },
            callbacks: { ...callbacks, success },
            // headers: { 'content-type': 'application/x-www-form-urlencoded' },
        });
    };
}
