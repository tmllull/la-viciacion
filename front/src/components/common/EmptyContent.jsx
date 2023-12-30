export default function EmptyContent({
    content = 'The content you are searching for returned an empty list. Check the filters and try it again.',
}) {
    return (
        <div className='empty-content-container'>
            <h3>Nothing to see here</h3>
            <p>{content}</p>
        </div>
    );
}
