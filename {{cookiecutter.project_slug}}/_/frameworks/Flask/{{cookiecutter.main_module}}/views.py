from flask import render_template

from {{ cookiecutter.main_module }} import app


@app.route("/")
def hello():
    return render_template('index.html')
