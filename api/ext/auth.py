from flask import request
from flask_rebar import HeaderApiKeyAuthenticator, messages, errors
from models import User


class Authentication(HeaderApiKeyAuthenticator):
    def __init__(self, header: str = 'Authorization', bearer: str = 'Token'):
        self.header = header
        self.bearer = bearer
        self.auth_service: Optional[AuthenticationService] = None
        super().__init__(header)

    def authenticate(self, header: str = 'Authorization'):
        auth_data = request.authorization
        user = User.objects(id=auth_data.user_id, password=auth_data.password).first()

        if user is None:
            raise errors.Unauthorized()
