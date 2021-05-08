import pytest
from mongoengine.errors import ValidationError


from models import User, Message

def test_message_create_success(mongoengine_connection):
    test_user = User(
        email='phipip@test.com',
        username='phipip.j.fry',
        password='ShutUpAndGetMyMoney'
    ).save()

    test_message = Message(
        text='Shut up and grab my money',
        user=test_user.pk
    ).save()

    assert Message.objects(id=test_message.pk) is not None

    

def test_message_create_fail(mongoengine_connection):
    with pytest.raises(ValidationError):
        test_user = User(
            email='phipip@test.com',
            username='phipip.j.fry',
            password='ShutUpAndGetMyMoney'
        ).save()
        
        test_message = Message(
            user=test_user.pk
        ).save()
