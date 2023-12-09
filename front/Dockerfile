# Stage 1 - Building image
FROM docker.io/node:20-slim as build-stage

WORKDIR /usr/src/app

COPY package.json .
COPY yarn.lock .

RUN yarn install

env VITE_API_URL=$API_URL

COPY src/ src/
COPY vite.config.js .
COPY index.html .

RUN ls -la

RUN npm run build

# Stage 2 - Running image
FROM nginx

COPY --from=build-stage /usr/src/app/dist /usr/share/nginx/html
COPY public/ /usr/share/nginx/html/public/
