from flask import current_app
from flask_rebar import Rebar
from flask_socketio import SocketIO


from config import settings
from ext.mongo_database import db
from ext.routes import api_v1
from models import User, Message
from schemas import MessageCreateSchema

rebar = Rebar()
socketio = SocketIO(cors_allowed_origins="*")


@api_v1.handles(
    method='POST',
    rule='/chat/message',
    request_body_schema=MessageCreateSchema(),
    response_body_schema=None
)
def send_message():
    data = rebar.validated_body
    message = Message(text=data.get('content'), user=data.get('user_id'))
    message.save()
    
    socketio = SocketIO(current_app, cors_allowed_origins="*")
    socketio.emit('broadcast_message', message.to_json(), broadcast=True)

    return {}, 200


# class ChatService(Namespace):
  
#     def on_list_messages(self, data):
#         messages = Message.objects().order_by('-timestamp')[:50]

#         emit('list_messages_reply', messages.to_json(), broadcast=True)

