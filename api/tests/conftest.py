import pytest
from mongoengine import connect, disconnect

from app import create_app

@pytest.fixture(scope='session')
def app():
    app = create_app(__name__)
    with app.app_context():
        yield app

@pytest.fixture()
def mongoengine_connection(app):
    disconnect()
    connection = connect(db='mongotest', host='mongomock://localhost')
    yield
    connection.drop_database('mongotest')
    disconnect()
