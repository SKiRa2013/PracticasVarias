FROM php:8.2-apache

# Instalamos las extensiones de PDO para MySQL
RUN docker-php-ext-install pdo pdo_mysql

# Habilitamos el módulo de reescritura de Apache (por si usas .htaccess)
RUN a2enmod rewrite