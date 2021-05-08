from marshmallow import fields, Schema


class UserCreateSchema(Schema):
    username = fields.String()
    email = fields.Email()
    password = fields.String()

class UserLoginSchema(Schema):
    id = fields.String()
    password = fields.String()


class UserSchema(Schema):
    id = fields.String()
    username = fields.String()


class MessageCreateSchema(Schema):
    user_id = fields.String()
    content = fields.String()

