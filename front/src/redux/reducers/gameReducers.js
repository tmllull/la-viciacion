import { initial, commonReducer, commonListReducer } from './commonReducers.js';
import { ACTIONS } from '../actions/gameActions.js';


export function games(state = initial, action) {
    return commonListReducer(state, action, ACTIONS.GET_GAMES);
}
