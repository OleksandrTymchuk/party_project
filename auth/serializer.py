from marshmallow import Schema, fields


class SignInSerializer(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


class TokenSerializer(Schema):
    token = fields.String(required=True)


class SignUpSerializer(Schema):
    id = fields.Integer(required=True, dump_only=True)
    email = fields.Email(required=True)
    name = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
