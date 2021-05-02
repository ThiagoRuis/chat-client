from models import User

def is_logged(function_to_decorate): #TODO improve this
    def is_logged_wrapper(*args):
        data = args[1]
        if 'user' in data:
            user_info = data.get('user')
            if User.objects(name=user_info.get('name')).first() is None:
                raise Exception
        function_to_decorate(*args)
    return is_logged_wrapper