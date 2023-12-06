import { useState } from 'react';
import { Container } from 'react-grid-easy';
import { useDispatch } from 'react-redux';
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { Toast } from 'primereact/toast';

import { login } from '/src/redux/actions/authActions.js';
import { useNavigation } from '/src/utils/navigationUtils.js';
import { APP_ROUTES } from '/src/constants/appRoutes.js';

export default function Login() {
    const dispatch = useDispatch();
    const { goToHomepage } = useNavigation();

    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });

    function handleLogin(event) {
        event.preventDefault();
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
        <Container className='login-page'>
            <form onSubmit={handleLogin}>

                <div className='p-inputgroup flex-1'>
                    <span className='p-inputgroup-addon'>
                        <i className='fa-solid fa-user' />
                    </span>
                    <InputText
                        onSubmit={handleLogin}
                        placeholder='Username'
                        value={formData.username}
                        id='username'
                        onChange={onChange}
                    />
                </div>
                <div className='p-inputgroup flex-1'>
                    <span className='p-inputgroup-addon'>
                        <i className='fa-solid fa-lock' />
                    </span>
                    <InputText
                        onSubmit={handleLogin}
                        placeholder='Password'
                        value={formData.password}
                        type='password'
                        id='password'
                        onChange={onChange}
                    />
                </div>
                <Button
                    label='Submit'
                    icon='fa-regular fa-check'
                    loading={loading}
                />
            </form>
        </Container>
    );
}
