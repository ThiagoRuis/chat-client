from dotenv import load_dotenv
import os

from flask_socketio import SocketIO, send, emit

from services import ChatService, IdentificationService, CommandService

load_dotenv()

def socket_conn():
    return SocketIO(cors_allowed_origins="*")

def initialize():
    socketio = socket_conn()
    socketio.on_namespace(ChatService('/chat'))
    socketio.on_namespace(IdentificationService('/identify'))
    socketio.on_namespace(CommandService('/command'))