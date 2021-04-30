from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

from chat import Chat

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

socketio.on_namespace(Chat('/'))


if __name__ == '__main__':
    socketio.run(app)
