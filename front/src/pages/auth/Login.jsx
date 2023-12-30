import { Button, Input }   from '@nextui-org/react';
import React, { useState } from 'react';
import { Container }       from 'react-grid-easy';
import { useDispatch }           from 'react-redux';
import { toast, ToastContainer } from 'react-toastify';

import { login } from '../../redux/actions/authActions.js';


import {
    errorAlert,
    successAlert,
} from '../../utils/notificationUtils.js';
import { useNavigation } from '../../utils/navigationUtils.js';


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
        errorAlert({
            text: "Login successful."
        })
        goToHomepage();
    }

    function onError(error) {
        setLoading(false);
        errorAlert("Authentication error.")
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
