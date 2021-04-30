from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('send_message')
def handle_message(data):
    print('received message: ' + data)

if __name__ == '__main__':
    socketio.run(app)