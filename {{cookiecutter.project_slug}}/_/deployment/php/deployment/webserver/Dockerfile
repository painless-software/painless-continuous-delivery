FROM php:7.0-apache
WORKDIR /var/www/html
COPY . .
RUN bash -c "source .envrc && inside_docker-moduser www-data && rm .envrc"
RUN docker-php-ext-install mysqli
RUN mv deployment/webserver/000-default.conf /etc/apache2/sites-available/ \
 && mv deployment/webserver/php.ini /usr/local/etc/php/ \
 && rm -r deployment \
 && chown -R www-data: .
