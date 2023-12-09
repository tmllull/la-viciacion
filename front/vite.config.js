import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
    server: {
        port: 8080,
    },
    build: {
        copyPublicDir: false,
    },
    plugins: [
        react(),
    ],
    resolve: {
        alias: {
            '@': 'src',
            src: 'src',
        },
    },
    define: {
        // By default, Vite doesn't include shims for NodeJS/
        // necessary dark-mode to work for some reason I don't understand
        global: {},
    },
});
