
export const initial = { isFetching: false, isError: false };

export function commonReducer(state = initial, action, actionType) {
    const requestAction = `${actionType}_request`;
    const fulFilledAction = `${actionType}_fulfilled`;
    const rejectedAction = `${actionType}_rejected`;
    const resetAction = `${actionType}_reset`;

    switch (action.type) {
        case requestAction: {
            return Object.assign({}, state, {
                isFetching: true,
                isError: false,
            });
        }
        case fulFilledAction: {
            return Object.assign({}, state, {
                isFetching: false,
                isError: false,
                item: action.payload.data,
            });
        }
        case rejectedAction:
            return Object.assign({}, state, {
                isFetching: false,
                isError: true,
                err: action.payload,
            });
        case resetAction: {
            return initial;
        }

        default:
            return state;
    }
}

export function commonListReducer(state = initial, action, actionType) {
    const requestAction = `${actionType}_request`;
    const fulFilledAction = `${actionType}_fulfilled`;
    const rejectedAction = `${actionType}_reject`;
    const resetAction = `${actionType}_reset`;
    switch (action.type) {
        case resetAction: {
            return Object.assign({}, state, {
                isFetching: true,
                isError: false,
                item: undefined,
            });
        }
        case requestAction: {
            return Object.assign({}, state, {
                isFetching: true,
                isError: false,
            });
        }
        case fulFilledAction: {
            if (action.onSuccess) {
                action.onSuccess(action.payload);
            }
            console.log(action.payload);
            // const oldContent = state.item && state.item.content || [];
            // const { pageNumber, content } = action.payload.data;
            const newState = {
                // pageNumber: state.item && state.item.pageNumber || pageNumber,
                cacheTime: Date.now() + 3600000, // adding 1 hour to the current date
                content: action.payload,
                // content: [
                //     ...oldContent,
                //     ...content,
                // ],
            };
            return Object.assign({}, state, {
                isFetching: false,
                isError: false,
                item: newState,
            });
        }
        case rejectedAction:

            if (action.onError) {
                action.onError(action.payload);
            }

            // if (action.silent === undefined || !action.silent) {
            //     let message = action.payload;
            //     manageErrorMessage('reducer-error', message);
            // }

            return Object.assign({}, state, {
                isFetching: false,
                isError: true,
                err: action.payload,
            });

        default:
            return state;
    }
}
