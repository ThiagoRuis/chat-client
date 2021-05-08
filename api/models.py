from datetime import datetime
from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    DateTimeField,
    ReferenceField,
    ListField,
    BooleanField,
    SequenceField,
    UUIDField
)


class User(Document):
    _id = UUIDField()
    email = StringField(required=True, unique=True)
    username = StringField()
    password = StringField()


class Message(Document):
    text = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)
    user = ReferenceField(User)


class Room(Document):
    name = StringField(required=True)
    users = ListField(ReferenceField(User))
