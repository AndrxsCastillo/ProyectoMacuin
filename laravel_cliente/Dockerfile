# ---- ETAPA 1: Compilar assets con Node ----
FROM node:20-slim AS node_builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY resources ./resources
COPY vite.config.js ./
COPY public ./public
RUN npm run build

# ---- ETAPA 2: PHP-FPM + Nginx ----
FROM php:8.2-fpm-alpine

RUN apk add --no-cache \
    nginx \
    git \
    curl \
    libpng-dev \
    oniguruma-dev \
    libxml2-dev \
    zip \
    unzip \
    libzip-dev \
    freetype-dev \
    libjpeg-turbo-dev

RUN docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd zip

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

COPY . .
COPY --from=node_builder /app/public/build ./public/build
COPY nginx.conf /etc/nginx/http.d/default.conf

RUN composer install --no-interaction --optimize-autoloader --no-dev

RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache \
    && chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache

EXPOSE 80

CMD ["sh", "-c", "sed -i \"s/listen 80/listen ${PORT:-80}/g\" /etc/nginx/http.d/default.conf && php-fpm -D && nginx -g 'daemon off;'"]
