FROM php:7.0-apache
WORKDIR /var/www/html
COPY . .
RUN . .envrc \
  && inside-docker_moduser www-data $LOCAL_UID $LOCAL_GID \
  && rm .envrc
RUN docker-php-ext-install mysqli
RUN mv config/webserver/000-default.conf /etc/apache2/sites-available/ \
 && mv config/webserver/php.ini /usr/local/etc/php/ \
 && rm -r config \
 && chown -R www-data: .
