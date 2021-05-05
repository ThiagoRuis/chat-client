from flask_rebar.errors import HttpJsonError


class HasNoUser(HttpJsonError):
    http_status_code, default_message = 402, "Payment Required"


class DuplicatedUser(HttpJsonError):
    http_status_code, default_message = 409, "Duplicated User"
