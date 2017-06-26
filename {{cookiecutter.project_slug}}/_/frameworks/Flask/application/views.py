"""
Views of the Flask application.
"""
# pylint: skip-file
from flask import render_template

from application import app


@app.route("/")
def hello():
    """
    Say hello using a template file.
    """
    return render_template('index.html')
