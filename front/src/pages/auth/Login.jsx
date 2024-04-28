import { Button, Input, Link } from '@nextui-org/react';
import React, { useState }     from 'react';
import { Col, Container }  from 'react-grid-easy';
import { useDispatch }     from 'react-redux';
import { useTranslation } from 'react-i18next';

import { login } from '../../redux/actions/authActions.js';


import {
    errorAlert,
    successAlert,
} from '../../utils/notificationUtils.js';
import { useNavigation } from '../../utils/navigationUtils.js';


export default function Login() {
    const dispatch = useDispatch();
    const { t, i18n } = useTranslation();
    const { goToHomepage, goToRegister } = useNavigation();

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
        successAlert(t('pages.auth.login.notifications.success'))
        goToHomepage();
    }

    function onError(error) {
        setLoading(false);
        errorAlert(t('pages.auth.login.notifications.error'))
    }


    return (
        <div className='auth-page'>
            <form className='auth-page__form' onSubmit={handleLogin}>
                <Container divisions={2}>
                    <h1 className='auth-page__title'>
                        {t('pages.auth.login.title')}
                    </h1>
                    <Col xs={2} sm={2}>
                        <Input
                            className='auth-page__form-input'
                            label={t('common.fields.username')}
                            labelPlacement='outside'
                            onSubmit={handleLogin}
                            onChange={onChange}
                            placeholder={t('common.fields.username')}
                            value={formData.username}
                            id='username'
                            startContent={
                                <i className='fa-solid fa-user' />
                            }
                        />
                    </Col>
                    <Col xs={2} sm={2}>
                        <Input
                            className='auth-page__form-input'
                            label={t('common.fields.password')}
                            type='password'
                            labelPlacement='outside'
                            onSubmit={handleLogin}
                            onChange={onChange}
                            placeholder={t('common.fields.password')}
                            value={formData.password}
                            id='password'
                            startContent={
                                <i className='fa-solid fa-lock' />
                            }
                        />
                    </Col>
                    <Col xs={2} sm={2} className='auth-page__actions'>
                        <Button
                            color='primary'
                            variant='shadow'
                            isLoading={loading}
                            type='submit'
                            onPress={handleLogin}
                        >
                            {t('common.buttons.login')}
                        </Button>
                        <Button
                            color='secondary'
                            showAnchorIcon
                            variant="solid"
                            onPress={goToRegister}
                        >
                            {t('pages.auth.actions.goToSignup')}
                        </Button>
                    </Col>
                </Container>
            </form>
        </div>
    );
}
