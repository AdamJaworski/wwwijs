from flask import Flask

from app.get import get
from app.post import post


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.register_blueprint(get)
    app.register_blueprint(post)

    return app
