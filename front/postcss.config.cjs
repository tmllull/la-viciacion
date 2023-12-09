module.exports = {
    plugins: {
        'postcss-import': {
            root: 'src/styles',
            path: 'src/styles',
            addModulesDirectories: ['src/styles']
        },
        'tailwindcss/nesting': 'postcss-nesting',
        tailwindcss: {},
        'postcss-preset-env': {
            features: { 'nesting-rules': false },
        },
        autoprefixer: {},
    },
};
