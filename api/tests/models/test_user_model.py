import pytest
from mongoengine.errors import ValidationError

from models import User

def test_user_create_success(mongoengine_connection):
    test_user = User(
        email='phipip@test.com',
        username='phipip.j.fry',
        password='ShutUpAndGetMyMoney'
    )
    test_user.save()
    assert User.objects(id=test_user.pk) is not None

def test_user_create_fail(mongoengine_connection):
    with pytest.raises(ValidationError):
        test_user = User(
            username='phipip.j.fry',
            password='ShutUpAndGetMyMoney'
        )
        test_user.save()
