import { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { Navigate, RouterProvider, useLocation, useRoutes } from 'react-router-dom';

import { getAuthenticatedStatus, getUserToken, removeUserToken } from '/src/utils/authUtils.js';
import { getAuthenticatedUser } from '/src/redux/actions/authActions.js';
import Spinner from '/src/components/common/Spinner.jsx';
import { APP_ROUTES } from '/src/constants/appRoutes.js';

import Home from '/src/pages/Home.jsx';
import Login from '/src/pages/auth/Login.jsx';


function routes(loggedUser) {
    return [
        {
            path: APP_ROUTES.HOME,
            element: loggedUser ? <Home /> : <Navigate to={APP_ROUTES.AUTH.LOGIN} />,
        },
        // AUTH ROUTES
        {
            path: APP_ROUTES.AUTH.LOGIN,
            element: loggedUser ? <Navigate to={APP_ROUTES.HOME} /> : <Login />,
        },
        {
            path: '*',
            element: <NotFound />,
        },
    ];
}

export default function AuthManager() {
    const [loggedIn, setLoggedIn] = useState(null);
    const [loading, setLoading] = useState(true);
    const dispatch = useDispatch();
    const location = useLocation();
    const routing = useRoutes(routes(loggedIn));


    function onPublicAccess() {
        setLoading(false);
        setLoggedIn(false);
    }
    function onAuthSuccess() {
        setLoggedIn(true);
        setLoading(false);
    }

    function onAuthRejected() {
        setLoading(false);
        removeUserToken();
        setLoggedIn(false);
    }

    useEffect(() => {
        console.log(`Location changed to ${location.pathname}`);
        setLoading(true);
        const authDataAvailable = getAuthenticatedStatus();
        if (authDataAvailable) {
            dispatch(getAuthenticatedUser({
                success: onAuthSuccess,
                error: onAuthRejected,
            }));
        } else {
            onPublicAccess();
        }
    }, [location.pathname]);

    if (loading) {
        return (
            <Spinner />
        );
    }
    return <>{routing}</>;
}

function NotFound() {
    return (
        <h1>404</h1>
    );
}
