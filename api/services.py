import json

from flask_socketio import Namespace, emit
from kombu import Connection
from pymongo.errors import DuplicateKeyError
from mongoengine import NotUniqueError 

from models import User, Message
from decorators import has_user
from api.tasks.tasks import get_stock_info
from api.exceptions import HasNoUser

class ChatService(Namespace):
    @has_user
    def on_send_message(self, data):
        email = data.get('user').get('email')
        user = User.objects(email=email).first()
        message = Message(text=data.get('msg'), user=user).save()

        emit('broadcast_message', message.to_json(), broadcast=True)

    def on_list_messages(self, data):
        messages = Message.objects().order_by('-timestamp')[:2]

        emit('list_messages_reply', messages.to_json(), broadcast=True)


class IdentificationService(Namespace):
    def on_login(self, data):
        if (user := User.objects(name=data.get('name')).first()) is None:
            user = User(**data).save()
            print(f'New User Created: {user.name}')
        msg = f'{user.name} connected!'
        emit('broadcast_message', msg, broadcast=True)
    
    def on_create_user(self, data):
        try:
            user = User(email=data.get('args')).save()
            emit('create_user_reply', user.to_json(), broadcast=True)
        except NotUniqueError:
            emit('create_user_reply', json.dumps({'error': 'Duplicated user'}), broadcast=True)
        except DuplicateKeyError:
            emit('create_user_reply', json.dumps({'error': 'Duplicated user'}), broadcast=True)
        except Exception:
            emit('create_user_reply', json.dumps({'error': 'Unknown Error'}), broadcast=True)

class CommandService(Namespace):
    def help(self):
        return """
            Welcome to Ruis ChatAPI!
            Commands
                /change_room room_name (Changes to selected room)
                /help (Displays the help info)
        """

    def on_help(self, data):
        emit('broadcast_message', self.help(), broadcast=True, namespace='chat')

    def on_stock(self, data):
        stock_code = data.get('msg')
        get_stock_info(stock_code)       

