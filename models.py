from datetime import datetime
from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    DateTimeField,
    EmbeddedDocumentField,
    ListField,
)


class User(EmbeddedDocument):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


class Message(Document):
    text = StringField()
    timestamp = DateTimeField(default=datetime.utcnow)
    user = EmbeddedDocumentField(User)


class Room(Document):
    name = StringField(required=True)
    users = ListField(EmbeddedDocumentField(User))
