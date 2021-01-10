FROM docker.io/library/python:3.9-alpine

ARG REQUIREMENTS=requirements.txt

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements* ./

RUN apk update \
 && apk add --no-cache \
    gettext \
    libjpeg \
    libpq \
    nginx \
 && apk add --no-cache --virtual .build-deps \
    build-base \
    git \
    jpeg-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    linux-headers \
    postgresql-dev \
    zlib-dev \
 && pip --no-cache-dir install --upgrade pip \
 && pip --no-cache-dir install -r ${REQUIREMENTS} \
 && apk del .build-deps \
 && ln -sfv /app/deployment/nginx.conf /etc/nginx/nginx.conf \
 && ln -sfv /dev/stdout /var/log/nginx/access.log \
 && ln -sfv /dev/stderr /var/log/nginx/error.log \
 && mkdir -v /run/nginx

COPY . .

# Support arbitrary user IDs (OpenShift guidelines)
RUN chown -R 1001:0 /app /run /var/lib/nginx \
 && chmod -R g=u    /app /run /var/lib/nginx /etc/passwd

USER 1001:0
{% if cookiecutter.framework == 'Django' %}
RUN DJANGO_SECRET_KEY=collectstatic \
    python manage.py collectstatic --noinput --link
{% endif %}
ENTRYPOINT ["./entrypoint.sh"]

CMD ["uwsgi", "deployment/uwsgi.ini"]
