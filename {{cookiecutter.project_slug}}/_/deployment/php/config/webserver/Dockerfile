FROM php:7.0-apache
RUN docker-php-ext-install mysqli
WORKDIR /var/www/html
COPY . .
RUN mv config/webserver/000-default.conf /etc/apache2/sites-available/ \
 && mv config/webserver/php.ini /usr/local/etc/php/ \
 && rm -r config
RUN chown -R www-data: .
