from flask_socketio import Namespace, emit


class Chat(Namespace):
    history = []
    def on_connect(self):
        emit('broadcast_message', self.history, broadcast=True)
        print('user connected')

    def on_disconnect(self):
        print('user disconnected')

    def on_send_message(self, data):
        print('received message: ' + data)
        self.history.append(data)
        emit('broadcast_message', data, broadcast=True)
