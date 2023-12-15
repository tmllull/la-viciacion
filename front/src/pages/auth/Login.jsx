import { Button, Input } from '@nextui-org/react';
import { useState } from 'react';
import { Container } from 'react-grid-easy';
import { useDispatch } from 'react-redux';

import { login } from '/src/redux/actions/authActions.js';
import { useNavigation } from '/src/utils/navigationUtils.js';


export default function Login() {
    const dispatch = useDispatch();
    const { goToHomepage } = useNavigation();

    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });

    function handleLogin(event) {
        if (typeof event?.preventDefault === 'function') {
            event.preventDefault();
        }
        setLoading(true);
        dispatch(login({
            data: formData,
            callbacks: {
                success: onSuccess,
                error: onError,
            },
        }));
    }

    function onChange({ target: { id, value } }) {
        const newData = { ...formData };
        newData[id] = value;
        setFormData(newData);
    }

    function onSuccess() {
        goToHomepage();
    }

    function onError() {
        setLoading(false);
    }


    return (
        <div className='login-page'>
            <form className='login-page__form' onSubmit={handleLogin}>
                <Container vertical divisions={3}>
                    <Input
                        className='login-page__form-input'
                        label='Username'
                        labelPlacement='outside'
                        onSubmit={handleLogin}
                        onChange={onChange}
                        placeholder='Username'
                        value={formData.username}
                        id='username'
                        startContent={
                            <i className='fa-solid fa-user' />
                        }
                    />
                    <Input
                        className='login-page__form-input'
                        label='Passwprd'
                        type='password'
                        labelPlacement='outside'
                        onSubmit={handleLogin}
                        onChange={onChange}
                        placeholder='Password'
                        value={formData.password}
                        id='password'
                        startContent={
                            <i className='fa-solid fa-lock' />
                        }
                    />
                    <Button
                        color='primary'
                        variant='shadow'
                        endContent={<i className='fa-regular fa-check' />}
                        isLoading={loading}
                        onPress={handleLogin}
                    >
                        Submit
                    </Button>
                </Container>
            </form>
        </div>
    );
}
