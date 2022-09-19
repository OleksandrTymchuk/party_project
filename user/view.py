import random

from flask import Blueprint

from core.auth import token_required
from core.database import db
from user.serializer import UserSerializer

user_router = Blueprint("user", __name__, url_prefix="/user")


@user_router.route("/profile")
@token_required
def profile(user):
    schema = UserSerializer()
    profile_json = schema.dump(user)
    return profile_json


@user_router.route("/telegram/connect")
@token_required
def telegram_connect(user):
    if not user.telegram_token:
        telegram_token = random.getrandbits(128)
        user.telegram_token = telegram_token
        db.session.add(user)
        db.session.commit()

    return f"https://telegram.me/mega_party_bot?start={user.telegram_token}"

