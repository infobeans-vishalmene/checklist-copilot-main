# frontend/Dockerfile
FROM node:18-alpine as build
WORKDIR /frontend
COPY package*.json ./
RUN npm install          # <-- fixed: use install instead of ci
COPY . .
RUN npm run build

