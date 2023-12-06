import { combineReducers } from 'redux';

import * as gameReducers from './gameReducers.js';
import * as layoutReducers from './layoutReducers';
import * as userReducers from './userReducers';


const hodState = combineReducers({
    ...gameReducers,
    ...layoutReducers,
    ...userReducers,
});

export default hodState;
