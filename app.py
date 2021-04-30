from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

from mongoengine import connect

from models import User
from chat import Chat

app = Flask(__name__)

# Application SETUP
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
connect('chat_api', username='appUser', password='passwordForAppUser', authentication_source='admin')

socketio.on_namespace(Chat('/'))

if __name__ == '__main__':
    socketio.run(app)
