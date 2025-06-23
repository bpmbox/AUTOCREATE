FROM php:8.2-fpm

# 作業ディレクトリ設定
WORKDIR /var/www

# システムパッケージの更新とインストール
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    libzip-dev \
    zip \
    unzip \
    nodejs \
    npm

# PHP拡張機能のインストール
RUN docker-php-ext-install \
    pdo_mysql \
    mbstring \
    exif \
    pcntl \
    bcmath \
    gd \
    zip

# Composerのインストール
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# ユーザー作成（権限管理用）
RUN groupadd -g 1000 www
RUN useradd -u 1000 -ms /bin/bash -g www www

# アプリケーションファイルをコピー
COPY . /var/www

# 権限設定
RUN chown -R www:www /var/www

# ユーザー切り替え
USER www

# ポート公開
EXPOSE 9000

# PHP-FPM起動
CMD ["php-fpm"]
