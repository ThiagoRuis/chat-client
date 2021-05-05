from flask import Flask
from dynaconf import FlaskDynaconf
from flask_rebar import Rebar

# from flask_socketio import SocketIO, emit
# from flask_login import LoginManager
# from ext.mongo_database import conn
# from services import ChatService, IdentificationService, CommandService
# from tasks.celeryconfig import Config

app = Flask(__name__)
FlaskDynaconf(app)
app.config.load_extensions()

# login = LoginManager(app)

# Application SETUP
# app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')

# #SocketIO initialization
# socketio_local = SocketIO(app, cors_allowed_origins="*")
# socketio_local.on_namespace(ChatService('/chat'))
# socketio_local.on_namespace(IdentificationService('/identify'))
# socketio_local.on_namespace(CommandService('/command'))

# if __name__ == '__main__':
#     socketio_local.run(app)

def create_app(name):
    app = Flask(name)
    rebar.init_app(app)
    return app


if __name__ == '__main__':
    create_app(__name__).run()