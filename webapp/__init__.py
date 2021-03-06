from flask import Flask

from webapp.db import db
from webapp.user.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    app.register_blueprint(user_blueprint)

    return app
