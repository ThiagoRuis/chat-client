from flask import Flask
from mongoengine import connect
from config import settings

db = connect(
    settings.MONGO_APP_DATABASE,
    username=settings.MONGO_APP_USER,
    password=settings.MONGO_APP_PASSWORD,
    authentication_source=settings.MONGO_APP_AUTH_SOURCE
)


def init_app(app: Flask):
    pass
