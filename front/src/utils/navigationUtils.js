import { useNavigate } from 'react-router-dom';

import { APP_ROUTES } from '../constants/appRoutes.js';


export function goToLogin(navigate) {
    navigate(APP_ROUTES.AUTH.LOGIN);
}

export function goToRegister(navigate) {
    navigate(APP_ROUTES.AUTH.REGISTER);
}

export function goToHomepage(navigate) {
    navigate(APP_ROUTES.HOME);
}


export function useNavigation() {
    const navigate = useNavigate();
    return {
        goToLogin: () => goToLogin(navigate),
        goToRegister: () => goToRegister(navigate),
        goToHomepage: () => goToHomepage(navigate),
    };
}
