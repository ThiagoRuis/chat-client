import json

from flask_socketio import Namespace, emit
from kombu import Connection

from models import User, Message
from decorators import is_logged
from api.tasks.tasks import get_stock_info


class ChatService(Namespace):
    #TODO: Check how to handle unknown command
    def on_connect(self):
        emit('stock', {}, namespace='command')
        print('ChatService connected')
        

    def on_disconnect(self):
        print('ChatService disconnected')

    @is_logged
    def on_send_message(self, data):
        username = data.get('user').get('name')
        user = User.objects(name=username).first()
        message = Message(text=data.get('msg'), user=user).save()

        emit('broadcast_message', message.to_json(), broadcast=True)

    def on_list_messages(self, data):
        messages = Message.objects().order_by('-timestamp')[:2]

        emit('list_messages_reply', messages.to_json(), broadcast=True)


class IdentificationService(Namespace):
    def on_connect(self):
        print('IdentificationService connected')

    def on_disconnect(self):
        print('IdentificationService disconnected')

    def on_login(self, data):
        if (user := User.objects(name=data.get('name')).first()) is None:
            user = User(**data).save()
            print(f'New User Created: {user.name}')
        msg = f'{user.name} connected!'
        emit('broadcast_message', msg, broadcast=True)


class CommandService(Namespace):
    def on_connect(self):
        print('CommandService connected')

    def on_disconnect(self):
        print('CommandService disconnected')

    def help(self):
        return """
            Welcome to Ruis ChatAPI!
            Commands
                /change_room room_name (Changes to selected room)
                /help (Displays the help info)
        """

    def on_help(self, data, connected_user=None):
        emit('broadcast_message', self.help(), broadcast=True, namespace='chat')

    def on_stock(self, data):
        stock_code = data.get('msg')
        get_stock_info(stock_code)
        
        print(f'called stock check to: {data}')
       


    def on_create_user(self, data, connected_user=None):
        new_user = User(name=data).save()

        msg = f'New User Created: {new_user.name}'
        emit('broadcast_message', msg, broadcast=True)
