# --- Build stage ---
FROM node:20-alpine AS build

WORKDIR /app

COPY client/package*.json ./
RUN npm ci

COPY client/ .

# If your API base URL is read at build time via import.meta.env, set it
# here so the build points at the nginx proxy path instead of a live domain.
ENV VITE_API_BASE_URL=/api

RUN npm run build

# --- Serve stage ---
FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY client/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
