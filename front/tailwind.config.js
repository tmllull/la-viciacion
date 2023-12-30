const { nextui } = require('@nextui-org/react');

const nextUiConfig = {
    themes: {
        dark: {
            colors: {
                background: '#1a1a1a',
            },
        },
    },
};

/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './index.html',
        './src/**/*.{js,ts,jsx,tsx}',
        './node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}',
    ],
    theme: {
        extend: {},
    },
    darkMode: 'class',
    plugins: [nextui(nextUiConfig)],
};
