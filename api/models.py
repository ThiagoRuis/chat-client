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
)


class User(Document):
    email = StringField(required=True, unique=True)
    username = StringField()
    password = StringField()
    id = SequenceField()
    is_authenticated = BooleanField(default=False)
    is_active = BooleanField()
    is_anonymous = BooleanField(default=True)

    def get_id(self):
        return id

    def save(self):
        self.is_anonymous = False
        Document.save(self)


class Message(Document):
    text = StringField()
    timestamp = DateTimeField(default=datetime.utcnow)
    user = ReferenceField(User)


class Room(Document):
    name = StringField(required=True)
    users = ListField(ReferenceField(User))
