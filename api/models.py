from datetime import datetime
from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    DateTimeField,
    ReferenceField,
    ListField,
)


class User(Document):
    email = StringField(required=True, unique=True)


class Message(Document):
    text = StringField()
    timestamp = DateTimeField(default=datetime.utcnow)
    user = ReferenceField(User)


class Room(Document):
    name = StringField(required=True)
    users = ListField(ReferenceField(User))
