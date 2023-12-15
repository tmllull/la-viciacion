import { createStore, applyMiddleware } from 'redux';
import { createLogger } from 'redux-logger';
import thunk from 'redux-thunk';
import { composeWithDevTools } from 'redux-devtools-extension';

import rootReducer from '../reducers';

const isProduction = import.meta.env.PROD;

let configureStore;
if (!isProduction) {
    const enhancer = composeWithDevTools(
        applyMiddleware(thunk, createLogger()),
    );

    configureStore = function configureStore(initialState) {
        return createStore(rootReducer, initialState, enhancer);
    };
} else {
    configureStore = function configureStore(initialState) {
        return createStore(rootReducer, initialState, applyMiddleware(thunk));
    };
}

export default configureStore;
