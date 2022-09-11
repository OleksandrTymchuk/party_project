from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from user.serializer import UserSerializer
from core.models.user_event import InvitationStatus


class EventSerializer(Schema):
    id = fields.Integer(required=True, dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    starts_at = fields.DateTime()
    ends_at = fields.DateTime()
    creator_id = fields.Integer()
    users = fields.List(fields.Nested(UserSerializer))


class EventInvitationSerializer(Schema):
    users_id = fields.List(fields.Integer)


class EventRespondSerializer(Schema):
    id = fields.Integer(required=True, dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    starts_at = fields.DateTime()
    ends_at = fields.DateTime()
    invitation_status = EnumField(enum=InvitationStatus, by_value=True)
