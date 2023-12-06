import React from 'react';
import ReactDOM from 'react-dom/client';
import { LocationProvider } from '@reach/router';
import { Provider } from 'react-redux';
import { BrowserRouter, RouterProvider } from 'react-router-dom';

// Prime styles
import 'primereact/resources/themes/soho-dark/theme.css';
import 'primereact/resources/primereact.min.css'; // core css
import 'primeflex/primeflex.css'; // flex
import 'primeflex/themes/primeone-dark.css';

import configureStore from '/src/redux/store';

import '/src/styles/index.scss';
import AppRouter from '/src/Router.jsx';

const store = configureStore();

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <Provider store={store}>
            <BrowserRouter>
                <AppRouter />
            </BrowserRouter>
        </Provider>
    </React.StrictMode>,
);
