export default function Spinner({
    inline = false,
}) {
    if (inline) {
        return (
            <span className='spinner inline-spinner' />
        );
    }
    return (
        <span className='spinner block-spinner' />
    );
}
