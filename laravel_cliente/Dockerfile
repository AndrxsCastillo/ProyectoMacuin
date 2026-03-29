FROM php:8.2-apache

# 2. Instalamos las dependencias del sistema requeridas por Laravel
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip \
    libzip-dev

# 3. Limpiamos la caché de apt para que la imagen sea más ligera
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# 4. Instalamos las extensiones de PHP necesarias para Laravel y MySQL
RUN docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd zip

# 5. Habilitamos el módulo "rewrite" de Apache (Súper importante para las rutas de Laravel)
RUN a2enmod rewrite

# 6. Cambiamos el "DocumentRoot" de Apache para que apunte a la carpeta /public de Laravel
ENV APACHE_DOCUMENT_ROOT /var/www/html/public
RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf
RUN sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf

# 7. Copiamos Composer desde su imagen oficial (para instalar las dependencias de Laravel)
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# 8. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /var/www/html

# 9. Copiamos todos los archivos de tu proyecto Laravel al contenedor
COPY . .

# 10. Instalamos las dependencias de PHP usando Composer
RUN composer install --no-interaction --optimize-autoloader --no-dev

# 11. Damos los permisos correctos a las carpetas que Laravel necesita modificar
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache
RUN chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache
