FROM node:16-alpine as build
WORKDIR /app
COPY app/package*.json .
RUN npm ci
COPY app .
RUN npm run build

FROM node:16-alpine as dev
WORKDIR /app
EXPOSE 8080
ENTRYPOINT [ "/app/entrypoint.sh" ]

FROM nginx:stable-alpine as prod
RUN mkdir /app
COPY --from=build /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080
