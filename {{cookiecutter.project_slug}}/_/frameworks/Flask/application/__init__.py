# pylint: disable=wrong-import-position
"""
The Flask application.

Taken from https://flask.palletsprojects.com/en/1.1.x/patterns/packages/
"""
{%- if cookiecutter.monitoring == 'Sentry' %}
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[FlaskIntegration()]
)
{% endif %}
from flask import Flask

app = Flask(__name__)

import application.views
