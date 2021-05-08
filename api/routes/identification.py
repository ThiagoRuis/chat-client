from pymongo.errors import DuplicateKeyError
from mongoengine import NotUniqueError
from flask_rebar import Rebar
from flask_rebar.errors import InternalError
from models import User, Message
from config import settings
from exceptions import HasNoUser, DuplicatedUser
from ext.mongo_database import db
from ext.routes import api_v1, authenticator
from schemas import (
    UserCreateSchema,
    UserSchema,
    UserLoginSchema,
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
    except (NotUniqueError, DuplicateKeyError) as err:
        raise DuplicatedUser
    except Exception as err:
        raise InternalError

@api_v1.handles(
    method='POST',
    rule='/identify/login',
    request_body_schema=UserLoginSchema(),
    response_body_schema=UserSchema(),
    # authenticators=[authenticator],
)
def login():
    from mongoengine import connect, disconnect
    from config import settings
    disconnect()
    dbz = connect(
        'HAH_AHAH',
        username='root',
        password='root',
        authentication_source=settings.MONGO_APP_AUTH_SOURCE
    )

    user = User(
        email='email@email.com',
        username='nomezao',
        password='passwordao'
    )
    user.save()

    pass
#         if (user := User.objects(name=data.get('name')).first()) is None:
#             user = User(**data).save()
#             print(f'New User Created: {user.name}')
#         msg = f'{user.name} connected!'
#         emit('broadcast_message', msg, broadcast=True)
