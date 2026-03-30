FROM php:8.2-apache

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    git curl libpng-dev libonig-dev \
    libxml2-dev zip unzip libzip-dev \
    nodejs npm \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar extensiones PHP
RUN docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd zip

# Habilitar mod_rewrite de Apache
RUN a2enmod rewrite

# Fijar MPM para evitar conflicto con nodejs
RUN a2dismod mpm_event mpm_worker || true && a2enmod mpm_prefork

# Apuntar Apache a /public de Laravel
ENV APACHE_DOCUMENT_ROOT /var/www/html/public
RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf
RUN sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf

# Instalar Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

# Copiar proyecto
COPY . .

# Instalar dependencias PHP
RUN composer install --no-interaction --optimize-autoloader --no-dev

# Compilar assets con Vite
RUN npm install && npm run build

# Permisos
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache
RUN chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache

EXPOSE 80

# Hacer que Apache use el puerto dinámico de Railway
CMD ["sh", "-c", "sed -i \"s/Listen 80/Listen ${PORT:-80}/g\" /etc/apache2/ports.conf && sed -i \"s/:80>/:${PORT:-80}>/g\" /etc/apache2/sites-available/000-default.conf && apache2-foreground"]
