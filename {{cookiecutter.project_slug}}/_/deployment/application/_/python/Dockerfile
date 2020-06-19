FROM docker.io/library/python:3.7-slim

ARG REQUIREMENTS=requirements.txt

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements* ./

RUN apt-get update \
 && apt-get install -y \
    gcc \
    gettext \
    libpq5 \
    libpq-dev \
    nginx \
    python3-dev \
 && pip --no-cache-dir install --upgrade pip \
 && pip --no-cache-dir install -r ${REQUIREMENTS} \
 && apt-get purge -y \
    gcc \
    libpq-dev \
    python3-dev \
 && apt-get autoremove -y --purge \
 && apt-get clean \
 && ln -sfv /app/deployment/webserver/nginx.conf /etc/nginx/nginx.conf \
 && ln -sfv /dev/stdout /var/log/nginx/access.log \
 && ln -sfv /dev/stderr /var/log/nginx/error.log

COPY . .

# Support arbitrary user IDs (OpenShift guidelines)
RUN chown -R 1001:0 /app /run /var/lib/nginx \
 && chmod -R g=u    /app /run /var/lib/nginx /etc/passwd

USER 1001:0
{% if cookiecutter.framework == 'Django' %}
RUN DJANGO_SECRET_KEY=collectstatic \
    python manage.py collectstatic --noinput --link
{% endif %}
ENTRYPOINT ["deployment/application/entrypoint.sh"]

CMD ["uwsgi", "deployment/application/uwsgi.ini"]
