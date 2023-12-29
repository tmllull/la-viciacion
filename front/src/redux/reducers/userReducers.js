import { initial, commonReducer } from './commonReducers.js';
import { ACTIONS as AUTH_ACTIONS } from '../actions/authActions.js';


export function authenticatedUser(state = initial, action) {
    return commonReducer(state, action, AUTH_ACTIONS.GET_AUTHENTICATED_USER);
}
