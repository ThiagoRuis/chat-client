from dotenv import load_dotenv
import os
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

from mongoengine import connect

from services import ChatService, IdentificationService, CommandService
from tasks.celeryconfig import Config

load_dotenv()
app = Flask(__name__)

# Application SETUP
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')

#Mongo connect
connect(os.getenv('APP_DATABASE'), username=os.getenv('APP_MONGO_USER'),
        password=os.getenv('APP_MONGO_PASS'), authentication_source='admin')

#SocketIO initialization

socketio_local = SocketIO(app, cors_allowed_origins="*")
socketio_local.on_namespace(ChatService('/chat'))
socketio_local.on_namespace(IdentificationService('/identify'))
socketio_local.on_namespace(CommandService('/command'))


if __name__ == '__main__':
    socketio.run(app)
