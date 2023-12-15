import { API_ENDPOINTS } from '/src/constants/apiEndpoints.js';
import { privateApi } from '/src/utils/axiosInstances.js';

import { deleteAction, getAction, postAction } from './commonActions';

// COMENT ACTION TYPES
export const ACTIONS = {
    GET_GAMES: 'fetch_games',
    FETCH_USER_BY_ID: 'fetch_user_by_id',
    UPLOAD_AVATAR: 'upload_avatar',
    UPDATE_PROFILE: 'update_profile',
    RESET_PASSWORD: 'reset_password',
    DELETE_USER: 'relete_user',
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

export function getGames(callbacks) {
    return function (dispatch) {
        getAction({
            type: ACTIONS.GET_GAMES,
            url: API_ENDPOINTS.GAMES.GAMES_LIST,
            instance: privateApi,
            dispatch,
            callbacks,
        });
    };
}
