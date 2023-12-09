import {
    Card, CardBody, CardFooter, CardHeader, Chip, Image,
} from '@nextui-org/react';
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Col } from 'react-grid-easy';

import AsyncListContainer from '/src/components/asyncComponents/AsyncListContainer.jsx';
import { getGames } from '/src/redux/actions/gameActions.js';

export default function Home() {
    const dispatch = useDispatch();

    const data = useSelector(store => store.games);

    useEffect(() => {
        dispatch(getGames());
    }, []);

    function renderItem({
        name,
        image_url: image,
        id,
        current_ranking: ranking,
        dev: developmentStudio,
        genres = [],
        played_time: playTime,
    }) {
        // Time is in seconds
        const parsedPlayTime = (playTime / 60 / 60).toFixed(2);
        return (
            <Col xs='12' sm='6' md='4' className='game-list_item' key={`GAME_${id}`}>
                <Card className='game-card py-4'>
                    <CardHeader className='pb-0 pt-2 px-4 flex-col items-start'>
                        <h4 className='game-card__name font-bold text-large'>{name}</h4>
                        <h5 className='game-card__developer text-medium'>{developmentStudio}</h5>
                        <div className='game-card__genres flex gap-1'>
                            {genres.split(',').map(genre => <Chip size='sm' key={`GAME_${id}_GENRE_${genre}`}>{genre}</Chip>)}
                        </div>
                    </CardHeader>
                    <CardBody className='overflow-visible flex justify-center'>
                        <Image
                            alt='Game image'
                            className='game-card__image object-cover rounded-xl'
                            src={image}
                        />
                    </CardBody>
                    <CardFooter className='game-card__statistics flex justify-between'>
                        <small className='game-card__ranking text-default-500'>
                            Ranking: <span className='font-bold'>#{ranking}</span>
                        </small>
                        <small className='game-card__play-time text-default-500'>
                            Play time: <span className='font-bold'>{parsedPlayTime}</span> Hours
                        </small>
                    </CardFooter>
                </Card>
            </Col>
        );
    }

    return (
        <AsyncListContainer
            data={data}
            renderItem={renderItem}
            className='game-list'
            title='Jugados en La viciación'
        />
    );
}
