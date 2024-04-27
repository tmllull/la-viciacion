import { Button, Input }              from '@nextui-org/react';
import React, { useEffect, useState } from 'react';
import { Col, Container }             from 'react-grid-easy';
import { useDispatch }     from 'react-redux';
import { useTranslation } from 'react-i18next';
import PasswordValidation from '../../components/PasswordValidation.jsx';

import { login, signup } from '../../redux/actions/authActions.js';
import {
    errorAlert,
    successAlert,
}                        from '../../utils/notificationUtils.js';
import { useNavigation } from '../../utils/navigationUtils.js';


export default function Register() {
    const dispatch = useDispatch();
    const { t, i18n } = useTranslation();
    const { goToHomepage, goToLogin } = useNavigation();

    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        repeatPassword: '',
        invitationKey: '',
    });
    const [passwordValidation, setPasswordValidation] = useState(false)

    function handleSignup(event) {
        if (typeof event?.preventDefault === 'function') {
            event.preventDefault();
        }
        setLoading(true);
        dispatch(signup({
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
        successAlert(t('pages.auth.signup.notifications.success'))
        goToHomepage();
    }

    function onError(error) {
        setLoading(false);
        errorAlert(t('pages.auth.signup.notifications.error'))
    }

    const validForm = passwordValidation && Object.values(formData).every(value => !!value && !!value.trim())
    return (
        <div className='auth-page'>
            <form className='auth-page__form' onSubmit={handleSignup}>
                <Container divisions={2}>
                    <h1 className='auth-page__title'>
                        {t('pages.auth.signup.title')}
                    </h1>
                    <Input
                        className='auth-page__form-input'
                        label={t('common.fields.username')}
                        labelPlacement='outside'
                        onSubmit={handleSignup}
                        onChange={onChange}
                        placeholder={t('common.fields.username')}
                        value={formData.username}
                        id='username'
                        startContent={
                            <i className='fa-solid fa-user' />
                        }
                    />
                    <Input
                        className='auth-page__form-input'
                        label={t('common.fields.email')}
                        labelPlacement='outside'
                        onSubmit={handleSignup}
                        onChange={onChange}
                        placeholder={t('common.fields.email')}
                        value={formData.email}
                        id='email'
                        startContent={
                            <i className="fa-solid fa-envelope"/>
                        }
                    />
                    <Input
                        className='auth-page__form-input'
                        label={t('common.fields.password')}
                        type='password'
                        labelPlacement='outside'
                        onSubmit={handleSignup}
                        onChange={onChange}
                        placeholder={t('common.fields.password')}
                        value={formData.password}
                        id='password'
                        startContent={
                            <i className='fa-solid fa-lock' />
                        }
                    />
                    <Input
                        className='auth-page__form-input'
                        label={t('common.fields.repeatPassword')}
                        type='password'
                        labelPlacement='outside'
                        onSubmit={handleSignup}
                        onChange={onChange}
                        placeholder={t('common.fields.repeatPassword')}
                        value={formData.repeatPassword}
                        id='repeatPassword'
                        startContent={
                            <i className='fa-solid fa-lock' />
                        }
                    />
                    <PasswordValidation
                        password={formData.password}
                        repeatPassword={formData.repeatPassword}
                        updateStatus={setPasswordValidation}
                    />
                    <Col xs={2} sm={2}>

                        <Input
                            className='auth-page__form-input'
                            label={t('common.fields.invitationKey')}
                            type='text'
                            labelPlacement='outside'
                            onSubmit={handleSignup}
                            onChange={onChange}
                            placeholder={t('common.fields.invitationKey')}
                            value={formData.invitationKey}
                            id='invitationKey'
                            startContent={
                                <i className='fa-light fa-key' />
                            }
                        />
                    </Col>
                    <div className='auth-page__actions'>
                        <Button
                            color='primary'
                            variant='shadow'
                            isLoading={loading}
                            isDisabled={!validForm}
                            type='submit'
                            onPress={handleSignup}
                        >
                            {t('common.buttons.signup')}
                        </Button>
                        <Button
                            color='secondary'
                            showAnchorIcon
                            variant="solid"
                            onPress={goToLogin}
                        >
                            {t('pages.auth.actions.goToLogin')}
                        </Button>
                    </div>
                </Container>
            </form>
        </div>
    );
}
