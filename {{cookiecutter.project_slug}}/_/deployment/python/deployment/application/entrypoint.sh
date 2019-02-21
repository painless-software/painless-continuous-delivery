#!/bin/sh
{% if cookiecutter.framework == 'Django' %}
python manage.py migrate
{%- endif %}
exec "$@"
