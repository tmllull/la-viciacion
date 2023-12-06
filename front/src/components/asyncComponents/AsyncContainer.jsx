import Spinner from 'src/components/common/Spinner';

/**
 * Redux commonReducer object structure.
 * @typedef {Object} commonReducerData
 * @property {boolean} isFetching - Determines if the data is being fetched.
 * @property {boolean} isError - Indicates when the latest data fetch attempt failed.
 * @property {Object} abortContoller - An abort controller used to abort previous request.
 */

/**
 * Async component allows rendering content dynamically based on the data status stored in redux.
 * @param {...commonReducerData | Array[commonReducerData]} data - Redux common reducer data object.
 * @param {React.JSX.Element} children - React element to render when the data is loaded.
 * @param {Boolean} renderOnError - Determines if the content is rendered when the data wasn't successfully fetched.
 * @returns {React.JSX.Element|*|null}
 * @constructor
 */
export default function AsyncContainer({
    renderOnError = false,
    children,
    data,
}) {
    let loaded = false;
    let error = false;
    let idle = false;
    const isArray = Array.isArray(data);
    if (isArray) {
        loaded = data.every(action => !action.isFetching);
        error = data.some(action => action.isError);
        idle = data.some(action => !action.isFetching && !action.item && !action.isError);
    } else {
        if (!data.isFetching && !data.item && !data.isError) {
            idle = true;
        }
        if (!data.isFetching && !data.isError && data.item) {
            loaded = true;
        } else if (data.isError) {
            error = true;
        }
    }
    if (idle) {
        return null;
    } if (loaded || data.item || (error && renderOnError)) {
        return children;
    } if (!loaded && !error) {
        return (
            <Spinner />
        );
    } if (error) {
        return (
            <h1>Ha habido un problemilla</h1>
        );
    }
}
