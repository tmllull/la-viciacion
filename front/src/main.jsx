import React from 'react';
import ReactDOM from 'react-dom/client';
import { NextUIProvider } from '@nextui-org/react';
import { I18nextProvider } from 'react-i18next';
import { ToastContainer } from 'react-toastify';

import './styles/index.css';
import App from './App.jsx';
import i18next from './utils/i18n.js'

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <ToastContainer />
        <NextUIProvider>
            <I18nextProvider i18n={i18next}>
                <App />
            </I18nextProvider>
        </NextUIProvider>
    </React.StrictMode>,
);
