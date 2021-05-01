import json

from flask_socketio import Namespace, emit

from models import User, Message
from stock_bot.services import stock_info

class Chat(Namespace):
    #TODO: Check how to handle unknown command
     
    def help(self):
        return """
            Welcome to Ruis ChatAPI!
            Commands
                /change_room room_name (Changes to selected room)
                /help (Displays the help info)
        """

    def on_connect(self):
        emit('help')  # TODO:check how to call another action
        print('user connected')

    def on_disconnect(self):
        print('user disconnected')

    def on_help(self, data, connected_user=None):
        emit('broadcast_message', self.help(), broadcast=True)

    def on_login(self, data):
        if (user := User.objects(name=data.get('name')).first()) is None:
            user = User(**data).save()
            print(f'New User Created: {user.name}')
        msg = f'{user.name} connected!'
        emit('broadcast_message', msg, broadcast=True)

    def on_stock(self, data, connected_user=None):
        stock_data = stock_info(data)
        print(f'called stock check to: {data}')
        emit('broadcast_message', json.dumps(stock_data), broadcast=True)

    def on_create_user(self, data, connected_user=None):
        new_user = User(name=data).save()

        msg = f'New User Created: {new_user.name}'
        emit('broadcast_message', msg, broadcast=True)

    def on_send_message(self, data, connected_user=None):
        message = Message(text=data)
        message.user = User.objects(name=user)[0]
        message.save()

        emit('broadcast_message', message, broadcast=True)
