import axios from 'axios';

import { publicApi } from '/src/utils/axiosInstances.js';

/**
 *
 * @param {string} type - base action type that will be used to dispatch redux actions.
 * @param {string} url - url where to send the get request.
 * @param {Object} params - Additional parameters to be sent with the request
 * @param {function} dispatch -dispatch function
 * @param {function} instance - axios instance constructor
 * @param {Object} options - Request options.
 * @param {Object} callbacks - Object containing the callbacks to be triggered.
 */
export function getAction({
    type,
    url,
    params,
    dispatch,
    instance = publicApi,
    options = { reset: false, update: false, fetch: true },
    callbacks = {},
}) {
    const requestAction = `${type}_request`;
    const fulfilledAction = `${type}_fulfilled`;
    const rejectedAction = `${type}_rejected`;
    const resetAction = `${type}_reset`;
    const updateAction = `${type}_update`;
    options.reset = options.reset ?? false;
    options.update = options.update ?? false;
    options.fetch = options.fetch ?? true;
    if (options.reset) {
        dispatch({ type: resetAction });
        if (callbacks.reset) {
            callbacks.reset();
        }
    }
    if (options.fetch) {
        dispatch({ type: requestAction });
        instance().get(url, {
            params,
        })
            .then((response) => {
                if (options.update) {
                    dispatch({
                        type: updateAction,
                        payload: response.data,
                    });
                } else {
                    dispatch({
                        type: fulfilledAction,
                        payload: response.data,
                    });
                }
                if (callbacks.success) {
                    callbacks.success(response.data);
                }
            })
            .catch((response) => {
                dispatch({
                    type: rejectedAction,
                    payload: response,
                });
                if (callbacks.error) {
                    callbacks.error(response);
                }
            });
    }
}

export function customGetAction(type, url, params, dispatch, onSuccess, onError) {
    const requestAction = `${type}_request`;
    const fulfilledAction = `${type}_fulfilled`;
    const rejectedAction = `${type}_rejected`;

    dispatch({ type: requestAction });
    axios.get(url, {
        params,
    })
        .then((response) => {
            dispatch({
                type: fulfilledAction,
                payload: response,
            });

            if (onSuccess) {
                onSuccess(response);
            }
        })
        .catch((err) => {
            dispatch({
                type: rejectedAction,
                payload: err,
            });

            if (onError) {
                onError(err);
            }
        });
}

export function postAction({
    type,
    url,
    data,
    dispatch,
    instance = publicApi,
    options = {
        reset: false,
        update: false,
        fetch: true,
    },
    callbacks = {},
    headers,
}) {
    const requestAction = `${type}_request`;
    const fulfilledAction = `${type}_fulfilled`;
    const rejectedAction = `${type}_rejected`;
    const resetAction = `${type}_reset`;
    const updateAction = `${type}_update`;

    // default data
    options.reset = options.reset !== undefined && options.reset || false;
    options.update = options.update !== undefined && options.update || false;
    options.fetch = options.fetch !== undefined && options.fetch || true;

    // initialize logic
    if (options.reset) {
        dispatch({ type: resetAction });
        if (callbacks.reset) {
            callbacks.reset();
        }
    }
    if (options.fetch) {
        dispatch({ type: requestAction });
        instance(headers).post(url, data)
            .then((response) => {
                if (options.update) {
                    dispatch({
                        type: updateAction,
                        payload: response.data,
                    });
                } else {
                    dispatch({
                        type: fulfilledAction,
                        payload: response.data,
                    });
                }
                if (callbacks.success) {
                    callbacks.success(response.data);
                }
            })
            .catch((response) => {
                console.log(response);
                dispatch({
                    type: rejectedAction,
                    payload: response,
                });

                if (callbacks.error) {
                    callbacks.error(response);
                }
            });
    }
}


export function putAction(type, url, data, dispatch, onSuccess, onError) {
    // console.log('listingAction type : ' + type);
    const requestAction = `${type}_request`;
    const fullfilledAction = `${type}_fulfilled`;
    const rejectedAction = `${type}_rejected`;

    dispatch({ type: requestAction });

    API().put(url, data)
        .then((response) => {
            dispatch({
                type: fullfilledAction,
                payload: response.data,
            });

            if (onSuccess) {
                onSuccess(response.data);
            }
        })
        .catch((err) => {
            dispatch({
                type: rejectedAction,
                payload: err,
            });

            if (onError) {
                onError(err);
            }
        });
}

export function deleteAction(type, url, data, dispatch, callbacks = {}) {
    const requestAction = `${type}_request`;
    const fulfilledAction = `${type}_fulfilled`;
    const rejectedAction = `${type}_rejected`;
    dispatch({ type: requestAction });
    API().delete(url, { data })
        .then((response) => {
            dispatch({
                type: fulfilledAction,
                payload: response.data,
            });
            if (callbacks.success) {
                callbacks.success(response.data);
            }
        })
        .catch(({ response: err }) => {
            dispatch({
                type: rejectedAction,
                payload: err.data,
            });
            if (callbacks.error) {
                callbacks.error(err.data);
            }
        });
}
