import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Col } from 'react-grid-easy';

import AsyncListContainer from '/src/components/asyncComponents/AsyncListContainer.jsx';
import { getGames } from '/src/redux/actions/gameActions.js';
import { publicApi } from '/src/utils/axiosInstances.js';
import EmptyContent from '/src/components/common/EmptyContent.jsx';
import { useNavigation } from '/src/utils/navigationUtils.js';

export default function Home() {
    const dispatch = useDispatch();

    const data = useSelector(store => store.games);
    const { goToLogin, goToHomepage } = useNavigation();

    useEffect(() => {
        dispatch(getGames());
    }, []);

    function renderItem(item, index) {
        console.log(item);
        return (
            <Col xs='12' sm='6' md='3' xl='2' className='game-list_item'>
                <img src={item.image_url} className='game-list_item-picture' />
                <h4 className='game-list_item-name'>{item.name}</h4>
            </Col>
        );
    }

    return (
        // <EmptyContent />
        <div>
            <img src='/public/react.svg' alt='' />
            <AsyncListContainer data={data} renderItem={renderItem} className='game-list' title='Games' />
        </div>
    );
}
