from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

from mongoengine import connect

from services import ChatService, IdentificationService, CommandService

app = Flask(__name__)

# Application SETUP
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
connect('chat_api', username='appUser', password='passwordForAppUser', authentication_source='admin')

socketio.on_namespace(ChatService('/chat'))
socketio.on_namespace(IdentificationService('/identify'))
socketio.on_namespace(CommandService('/command'))

if __name__ == '__main__':
    socketio.run(app)
