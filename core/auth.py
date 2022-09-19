import jwt
from flask import request

from config import Config
from core.models.user import User


def token_required(f):
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get("Authorization")
        telegram_token = request.headers.get("auth_telegram_token")

        if auth_token:
            data = jwt.decode(auth_token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data["user_id"]).first()
        elif telegram_token:
            current_user = User.query.filter_by(telegram_token=telegram_token).first()
        else:
            return {"error": "Token required"}, 401
        return f(current_user, *args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper
