from dotenv import load_dotenv
import os

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from flask_login import LoginManager

from mongo_database import conn
from services import ChatService, IdentificationService, CommandService
from tasks.celeryconfig import Config

load_dotenv()
app = Flask(__name__)
login = LoginManager(app)

# Application SETUP
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')

#Mongo connect
conn()
#SocketIO initialization

socketio_local = SocketIO(app, cors_allowed_origins="*")
socketio_local.on_namespace(ChatService('/chat'))
socketio_local.on_namespace(IdentificationService('/identify'))
socketio_local.on_namespace(CommandService('/command'))

@app.route('/')
def hello_world():
    socketio_local.emit('teste', {"teste":"DO SERVIDOR"},namespace='/chat')
    return 'Hello, World!'


if __name__ == '__main__':
    socketio_local.run(app)
