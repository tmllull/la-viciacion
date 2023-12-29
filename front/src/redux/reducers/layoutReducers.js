import { actions } from '../actions/layoutActions';

export function sidebarStatus(state = false, action) {
    switch (action.type) {
        case actions.TOGGLE_SIDEBAR: {
            return !state;
        }
        case actions.OPEN_SIDEBAR: {
            return true;
        }
        case actions.CLOSE_SIDEBAR: {
            return false;
        }
        default: {
            return state;
        }
    }
}
