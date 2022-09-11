from marshmallow import Schema, fields


class UserSerializer(Schema):
    id = fields.Integer(required=True, dump_only=True)
    email = fields.Email(required=True, dump_only=True)
    name = fields.String(required=True, dump_only=True)
