from flask import Flask

app = Flask(__name__)  # noqa

import application.views  # noqa
