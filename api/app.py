from flask import Flask
from dynaconf import FlaskDynaconf




def create_app(name):
    app = Flask(__name__)
    FlaskDynaconf(app)
    app.config.load_extensions()
    return app


if __name__ == '__main__':
    create_app(__name__).run()
