FROM php:7.0-apache
RUN docker-php-ext-install mysqli
COPY config/webserver/php.ini /usr/local/etc/php/
COPY . /var/www/html/
RUN rm -r /var/www/html/config
