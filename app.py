from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

from mongoengine import connect

from services import ChatService, IdentificationService, CommandService

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

# #SocketIO for external commands
# socketio_external = SocketIO(cors_allowed_origins="*", message_queue='amqp://guest:guest@localhost:5672/chat_api//')
# socketio_external.on_namespace(ChatService('/chat'))
# socketio_external.on_namespace(IdentificationService('/identify'))
# socketio_external.on_namespace(CommandService('/command'))

if __name__ == '__main__':
    socketio.run(app)
