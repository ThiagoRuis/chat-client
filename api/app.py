from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

from mongoengine import connect

from services import ChatService, IdentificationService, CommandService
from api.tasks.celeryconfig import Config

app = Flask(__name__)

# Application SETUP
app.config['SECRET_KEY'] = 'secret!'

#Mongo connect
connect('chat_api', username='appUser',
        password='passwordForAppUser', authentication_source='admin')

#SocketIO initialization

socketio_local = SocketIO(app, cors_allowed_origins="*")
socketio_local.on_namespace(ChatService('/chat'))
socketio_local.on_namespace(IdentificationService('/identify'))
socketio_local.on_namespace(CommandService('/command'))


if __name__ == '__main__':
    socketio.run(app)
