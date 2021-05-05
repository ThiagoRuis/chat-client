# import json
# from flask_socketio import Namespace, emit
# from kombu import Connection
# from decorators import has_user
# from tasks.tasks import get_stock_info

from pymongo.errors import DuplicateKeyError
from mongoengine import NotUniqueError
from flask_rebar import Rebar
from flask_rebar.errors import InternalError

from models import User, Message
from config import settings
from exceptions import HasNoUser, DuplicatedUser
from ext.routes import api_v1
from schemas import (
    UserCreateSchema,
    UserSchema,
)

rebar = Rebar()


@api_v1.handles(
    method='POST',
    rule='/identify/create_user',
    request_body_schema=UserCreateSchema(),
    response_body_schema=UserSchema(),
)
def create_user():
    try:
        data = rebar.validated_body
        user = User(
            email=data.get('email'),
            username=data.get('username'),
            password=data.get('password')
        )
        user.save()
        return {"id": user.pk, "username": user.username}, 200
    except NotUniqueError:
        raise DuplicatedUser
    except DuplicateKeyError:
        raise DuplicatedUser
    except Exception:
        raise InternalError


# class ChatService(Namespace):
#     @has_user
#     def on_send_message(self, data):
#         email = data.get('user').get('email')
#         user = User.objects(email=email).first()
#         message = Message(text=data.get('msg'), user=user).save()

#         emit('broadcast_message', message.to_json(), broadcast=True)

#     def on_list_messages(self, data):
#         messages = Message.objects().order_by('-timestamp')[:50]

#         emit('list_messages_reply', messages.to_json(), broadcast=True)


# class IdentificationService(Namespace):
#     def on_login(self, data):
#         if (user := User.objects(name=data.get('name')).first()) is None:
#             user = User(**data).save()
#             print(f'New User Created: {user.name}')
#         msg = f'{user.name} connected!'
#         emit('broadcast_message', msg, broadcast=True)


# class CommandService(Namespace):
#     def help(self):
#         return """
#             Welcome to Ruis ChatAPI!
#             Commands
#                 /change_room room_name (Changes to selected room)
#                 /help (Displays the help info)
#         """

#     def on_help(self, data):
#         emit('broadcast_message', self.help(), broadcast=True, namespace='chat')

#     def on_stock(self, data):
#         stock_code = data.get('msg')
#         get_stock_info(stock_code)
