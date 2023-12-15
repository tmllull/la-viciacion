import { initial, commonReducer, commonListReducer } from '/src/redux/reducers/commonReducers.js';
import { ACTIONS } from '/src/redux/actions/gameActions.js';


export function games(state = initial, action) {
    return commonListReducer(state, action, ACTIONS.GET_GAMES);
}
