from flask_socketio import Namespace, emit


class Chat(Namespace):
    def on_send_message(self, data):
        print('received message: ' + data)
        emit('broadcast_message', data, broadcast=True)
