from marshmallow import Schema, fields

class UserSchema(Schema):
    user_id = fields.Int(data_key="userID")
    username = fields.String()

class UserListSchema(Schema):
    users = fields.List(fields.Nested(UserSchema))