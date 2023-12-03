# Stage 1 - Building image
FROM node as build-stage

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm config set fetch-retry-maxtimeout 600000
RUN npm install

COPY . .

RUN npm run build

# Stage 2 - Running image
FROM nginx

COPY --from=build-stage /usr/src/app/build /usr/share/nginx/html