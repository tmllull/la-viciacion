

export const actions = {
    TOGGLE_SIDEBAR: 'toggle-sidebar',
    OPEN_SIDEBAR: 'open-sidebar',
    CLOSE_SIDEBAR: 'close_sidebar',
};

export function toggleSidebarStatus(status) {
    return function (dispatch) {
        if (status) {
            dispatch({
                type: actions[`${status}_SIDEBAR`],
            });
        } else {
            dispatch({
                type: actions.TOGGLE_SIDEBAR,
            });
        }
    };
}
