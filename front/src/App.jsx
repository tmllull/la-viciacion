import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import useDarkMode from 'use-dark-mode';

import AppRouter from '/src/Router.jsx';
import configureStore from '/src/redux/store';

const store = configureStore();

function App() {
    const darkMode = useDarkMode(true);

    return (
        <Provider store={store}>
            <main className={`${darkMode.value ? 'dark' : ''} main-container text-foreground bg-background`}>
                <BrowserRouter>
                    <AppRouter />
                </BrowserRouter>
            </main>
        </Provider>
    );
}

export default App;
