from flask import Flask
from flask_socketio import SocketIO
from services import ChatService



def init_app(app: Flask):
    socketio = SocketIO(app, cors_allowed_origins="*")
    # Socket endpoints initialization
    socketio.on_namespace(ChatService('/chat'))
    socketio.run(app)
