from models import User
from exceptions import HasNoUser 

def has_user(function_to_decorate): #TODO improve this
    def has_user_wrapper(*args):
        data = args[1]
        if 'user' in data:
            user_info = data.get('user')
            if User.objects(email=user_info.get('email')).first() is None:
                raise HasNoUser
        function_to_decorate(*args)
    return has_user_wrapper
