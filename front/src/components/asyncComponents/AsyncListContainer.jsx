import Spinner from '/src/components/common/Spinner';
import { Container, Grid } from 'react-grid-easy';
import EmptyContent from '/src/components/common/EmptyContent';

/**
 * Redux commonReducer object structure.
 * @typedef {Object} commonReducerData
 * @property {boolean} isFetching - Determines if the data is being fetched.
 * @property {boolean} isError - Indicates when the latest data fetch attempt failed.
 * @property {Object} abortContoller - An abort controller used to abort previous request.
 */


/**
 * Async list component allows rendering content dynamically based on the data status stored in redux.
 * @param {...commonReducerData} data - Redux common reducer data object.
 * @param {function} renderItem - Function called to render each element on the list.
 * @param {function} loadPage - Function called when the trigger to load more data is reached.
 * @param {string} title - Title to be shown on the top of the list.
 * @param {string} emptyContent
 * @returns {React.JSX.Element|*|null}
 * @constructor
 */
export default function AsyncListContainer({
    data,
    renderItem,
    loadPage,
    title = 'This title needs to change',
    emptyContent,
}) {
    // const [spying, setSpying] = useState(false);
    // const [page, setPage] = useState(false)
    //
    // function handleScrollCapture() {
    //     try {
    //         const currentScroll = document.scrollingElement.scrollTop + window.innerHeight;
    //         const spyPosition = document.getElementById('scroll-spy').offsetTop;
    //         if (parseInt(currentScroll) >= parseInt(spyPosition - 200)) {
    //             loadPage();
    //         }
    //     } catch {
    //
    //     }
    // }
    //
    // useEffect(() => {
    //     if (data.pageNumber > 1) {
    //         window.addEventListener('scroll', handleScrollCapture);
    //         setSpying(true)
    //     }
    // })
    //
    // useEffect(() => {
    //     if (data.item && data.pageNumber > 1 && !spying) {
    //         window.addEventListener('scroll', handleScrollCapture);
    //         this.setState({
    //             spying: true
    //         })
    //     } else if (props.data.item && data.pageNumber === page) {
    //         if (this.props.data.pageNumber > 1) {
    //             window.addEventListener('scroll', handleScrollCapture);
    //         }
    //     }
    //     return function unmount() {
    //         if (data.pageNumber > 1) {
    //             window.removeEventListener('scroll', handleScrollCapture);
    //         }
    //     }
    // }, [JSON.stringify(data)]);
    if (!data.isFetching && !data.item) {
        return null;
    } if (data.isFetching && !data.item) {
        return (
            <Spinner />
        );
    } if (data.isError) {
        return (
            <h1>Ha habido un problemilla</h1>
        );
    } if (data?.item?.content?.length === 0) {
        return (
            <Container className='async-list-container' columns={12}>
                <h1>{title}</h1>
                <EmptyContent content={emptyContent} />
            </Container>
        );
    }
    return (
        <Container columns='12'>
            <h1>{title}</h1>
            {data.item.content.map((item, index) => {
                if (typeof renderItem === 'function') {
                    return renderItem(item, index);
                }
                // MORE TYPES CAN BE ADDED
                return null;
            })}
            {/*
                    {data.item.pageNumber > page &&
                        <div id='scroll-spy' onScroll={this.handleScrollCapture} />
                    }
*/}
            {data.isFetching
                        && <Spinner />
                    }
        </Container>
    );
}
