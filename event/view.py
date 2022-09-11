import http

from flask import Blueprint, request, jsonify

from core.auth import token_required
from core.database import db
from core.models import Event, User, UserEvent
from event.serializer import EventSerializer, EventInvitationSerializer, EventRespondSerializer

event_router = Blueprint("event", __name__, url_prefix="/event")


@event_router.route("", methods=["GET"])
@token_required
def get(user):
    schema = EventSerializer(many=True)
    events = Event.query.filter(
        Event.users.any(
            User.id == user.id
        )
    )
    events_json = schema.dump(events)
    return jsonify(events_json)


@event_router.route("/<int:event_id>", methods=["GET"])
@token_required
def retrieve(user, event_id):
    schema = EventSerializer()
    event = Event.query.filter(
        Event.users.any(
            User.id == user.id
        )
    ).filter(Event.id == event_id).first()
    events_json = schema.dump(event)
    return jsonify(events_json)


@event_router.route("", methods=["POST"])
@token_required
def create(user):
    data = request.get_json()
    schema = EventSerializer()
    event_data = schema.load(data)
    event_obj = Event(
        name=event_data["name"],
        description=event_data["description"],
        starts_at=event_data["starts_at"],
        ends_at=event_data["ends_at"],
        creator_id=user.id
    )
    event_obj.users.append(user)
    db.session.add(event_obj)
    db.session.commit()
    event_json = schema.dump(event_obj)
    return event_json


@event_router.route("/<int:event_id>/invite", methods=["POST"])
@token_required
def invite(user, event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event.creator_id == user.id:
        data = request.get_json()
        event_schema = EventSerializer()
        invitation_schema = EventInvitationSerializer()
        invitation_data = invitation_schema.load(data)
        event = Event.query.filter(
            Event.users.any(
                User.id == user.id
            )
        ).filter(Event.id == event_id).first()
        if not event:
            return "No event found"

        for user_id in invitation_data["users_id"]:
            invited_user = User.query.get(user_id)
            if invited_user:
                event.users.append(invited_user)

        db.session.add(event)
        db.session.commit()
        event_json = event_schema.dump(event)
        return event_json
    else:
        return "Permission denied", 403


@event_router.route("/<int:event_id>/respond", methods=["POST"])
@token_required
def respond_to_invitation(user, event_id):
    data = request.get_json()

    if data["invitation_status"] not in ["accepted", "declined"]:
        data["invitation_status"] = "pending"

    respond_schema = EventRespondSerializer()
    event_data = UserEvent.query.filter_by(user_id=user.id, event_id=event_id).first()
    respond_data = respond_schema.load(data)
    event_data.invitation_status = respond_data["invitation_status"]
    db.session.add(event_data)
    db.session.commit()
    event_respond_json = respond_schema.dump(event_data)
    return event_respond_json


@event_router.route("/<int:event_id>", methods=["PUT"])
@token_required
def edit(user, event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event.creator_id == user.id:
        data = request.get_json()
        schema = EventSerializer()
        event_data = schema.load(data)
        event = Event.query.filter(
            Event.users.any(
                User.id == user.id
            )
        ).filter(Event.id == event_id).first()
        event.name = event_data["name"],
        event.description = event_data["description"],
        event.starts_at = event_data["starts_at"],
        event.ends_at = event_data["ends_at"],
        event.creator_id = user.id
        event.users.append(user)
        db.session.add(event)
        db.session.commit()
        event_json = schema.dump(event)
        return event_json
    else:
        return "Permission denied", 403


@event_router.route("/<int:event_id>", methods=['DELETE'])
@token_required
def delete(user, event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event.creator_id == user.id:
        UserEvent.query.filter_by(event_id=event_id).delete()
        Event.query.filter_by(id=event_id).delete()
        db.session.commit()
        return {}, http.HTTPStatus.NO_CONTENT
    else:
        return "Permission denied", 403
