import datetime

import jwt
from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash

from auth.serializer import SignUpSerializer, SignInSerializer, TokenSerializer
from config import Config
from core.database import db
from core.models.user import User

auth_router = Blueprint("auth", __name__, url_prefix="/auth")


@auth_router.route("/signin", methods=['POST'])
def signin():
    data = request.get_json()
    schema = SignInSerializer()
    user_data = schema.load(data)

    if user := User.query.filter_by(email=user_data.get("email")).first():
        if check_password_hash(user.password, user_data.get("password")):
            token = jwt.encode(
                {
                    "user_id": user.id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # expiration dateline
                },
                Config.SECRET_KEY,
                algorithm="HS256"
            )
            token_schema = TokenSerializer()
            token_json = token_schema.dump({"token": token})
            return token_json
        else:
            return {"error": "User not found"}, 401
    else:
        return {"error": "User not found"}, 401


@auth_router.route("/signup", methods=['POST'])
def signup():
    data = request.get_json()
    schema = SignUpSerializer()

    user_data = schema.load(data)
    pass_hash = generate_password_hash(user_data.get("password"))
    new_user = User(email=user_data["email"], name=user_data["name"], password=pass_hash)
    db.session.add(new_user)
    db.session.commit()

    new_user_json = schema.dump(new_user)
    return new_user_json, 201
