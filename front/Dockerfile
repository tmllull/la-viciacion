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
COPY postcss.config.cjs .
COPY tailwind.config.js .

RUN npm run build

# Stage 2 - Running image
FROM nginx:1.25-alpine
COPY --from=build-stage --chown=nginx /usr/src/app/dist /usr/share/nginx/html
COPY ./config/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./config/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf
COPY public/ /usr/share/nginx/html/public/

USER nginx
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
