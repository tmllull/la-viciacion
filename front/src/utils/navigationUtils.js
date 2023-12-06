import { APP_ROUTES } from '/src/constants/appRoutes.js';
import { useNavigate } from 'react-router-dom';


export function goToLogin(navigate) {
    navigate(APP_ROUTES.AUTH.LOGIN);
}

export function goToHomepage(navigate) {
    navigate(APP_ROUTES.HOME);
}


export function useNavigation() {
    const navigate = useNavigate();
    return {
        goToLogin: () => goToLogin(navigate),
        goToHomepage: () => goToHomepage(navigate),
    };
}
