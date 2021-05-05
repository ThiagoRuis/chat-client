from marshmallow import fields, Schema


class UserCreateSchema(Schema):
    username = fields.String()
    email = fields.Email()
    password = fields.String()


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
