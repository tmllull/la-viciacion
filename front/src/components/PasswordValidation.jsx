import { useEffect, useState } from 'react';
import { useTranslation }      from 'react-i18next';

function validateLength(password) {
    return password.length >= 12 && password.length <= 24;
}

const validationRegex = {
    lowercase: /^.*[a-z].*$/,
    uppercase: /^.*[A-Z].*$/,
    numbers: /^.*[0-9].*$/,
    special: /^.*[!@#$%^&*].*$/
}

export default function PasswordValidation({
    updateStatus,
    password,
    repeatPassword
}) {
    const {t} = useTranslation()
    const [validations, setValidations] = useState({
        length: false,
        lowercase: false,
        uppercase: false,
        numbers: false,
        special: false,
        repeat: false,
    })

    useEffect(() => {
        const newState = {
            length: validateLength(password),
            repeat: password === repeatPassword && !!password,
        }
        Object.entries(validationRegex)
            .forEach(([key, value]) => {
                newState[key] = value.test(password)
        })
        updateStatus(Object.values(newState).every(value => value))
        setValidations(newState)
    }, [password, repeatPassword]);

    return (
        <div className='password-validation'>
            <h4 className='password-validation_title'>{t('components.auth.passwordValidation.title')}</h4>
            <div className='password-validation_entries'>
                {...Object.entries(validations).map(([key, status]) => {
                    const statusClass = status ? 'text-success-500' : 'text-danger-500';
                    return (
                        <div className={`password-validation_entry ${statusClass}`}>
                            <i className={`fa-regular ${status ? 'fa-check' : 'fa-xmark'}`} />
                            <p>{t(`components.auth.passwordValidation.fields.${key}`)}</p>
                        </div>
                    )
                })}
            </div>
        </div>
    );
}
