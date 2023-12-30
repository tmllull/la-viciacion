import React from 'react';
import ReactDOM from 'react-dom/client';
import { NextUIProvider } from '@nextui-org/react';

import './styles/index.css';
import { ToastContainer } from 'react-toastify';
import App from './App.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <ToastContainer />
        <NextUIProvider>
            <App />
        </NextUIProvider>
    </React.StrictMode>,
);
