from flask import Flask
app = Flask(__name__)  # noqa

import {{ cookiecutter.main_module }}.views  # noqa
