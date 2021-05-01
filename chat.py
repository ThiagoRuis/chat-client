from flask_socketio import Namespace, emit

from models import User, Message


class Chat(Namespace):
    def help(self):
        return """
            Welcome to Ruis ChatAPI!
            Commands
                /change_room room_name (Changes to selected room)
                /help (Displays the help info)
        """

    def on_connect(self, user=None):
        emit('broadcast_message', self.help(), broadcast=True)
        print('user connected')

    def on_disconnect(self, user=None):
        print('user disconnected')

    def on_help(self, data, user=None):
        emit('broadcast_message', self.help(), broadcast=True)

    def on_stock(self, data, user=None):
        print(f'called stock check to: {data}' )

    def on_create_user(self, data, user=None):
        new_user = User(name=data).save()

        msg = f'New User Created: {new_user.name}'
        emit('broadcast_message', msg, broadcast=True)

    def on_send_message(self, data, user=None):
        message = Message(text=data)
        message.user = User.objects(name=user)[0]                                                    
        message.save()

        emit('broadcast_message', message, broadcast=True)
