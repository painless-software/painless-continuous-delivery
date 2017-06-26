"""
The Flask application.

Taken from http://flask.pocoo.org/docs/0.12/patterns/packages/
"""
from flask import Flask

app = Flask(__name__)  # noqa, pylint: disable=invalid-name

import application.views  # noqa, pylint: disable=wrong-import-position
