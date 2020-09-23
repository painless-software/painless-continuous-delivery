"""
The Flask application.

Taken from https://flask.palletsprojects.com/en/1.1.x/patterns/packages/
"""
from flask import Flask

app = Flask(__name__)  # noqa, pylint: disable=invalid-name

import application.views  # noqa, pylint: disable=wrong-import-position
