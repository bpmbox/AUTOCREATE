FROM php:8.2-fpm

# 🔧 System dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip \
    libzip-dev \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd zip

# 📦 Composer installation
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# 👤 User creation
RUN groupadd -g 1000 www
RUN useradd -u 1000 -ms /bin/bash -g www www

# 📁 Working directory
WORKDIR /var/www/html

# 🔐 Permissions
RUN chown -R www:www /var/www/html
RUN chmod -R 755 /var/www/html/storage
RUN chmod -R 755 /var/www/html/bootstrap/cache

# 👤 Switch to www user
USER www

# 🚀 PHP-FPM configuration
EXPOSE 9000

CMD ["php-fpm"]
