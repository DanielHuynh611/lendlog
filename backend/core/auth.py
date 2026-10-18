"""Password hashing, signed JWT authentication and browser CSRF protection."""
import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, g, jsonify, redirect, request, session
from sqlalchemy import select

from backend.core.db import get_engine, users

AUTH_COOKIE = "lendlog_auth"
TOKEN_SECONDS = 86400


def _encode_segment(value):
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _decode_segment(value):
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def hash_password(password):
    salt = secrets.token_bytes(16)
    rounds = 310000
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, rounds)
    return f"pbkdf2_sha256$310000${_encode_segment(salt)}${_encode_segment(digest)}"


def verify_password(password, encoded):
    try:
        algorithm, rounds, salt, expected = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), _decode_segment(salt), int(rounds)
        )
        return hmac.compare_digest(actual, _decode_segment(expected))
    except (TypeError, ValueError):
        return False


def issue_token(subject, *, expires_in_seconds=TOKEN_SECONDS):
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {"sub": subject, "iss": current_app.config["JWT_ISSUER"],
         "iat": now, "exp": now + timedelta(seconds=expires_in_seconds)},
        current_app.config["JWT_SECRET"], algorithm="HS256",
    )


def _verify_token(token):
    return jwt.decode(
        token, current_app.config["JWT_SECRET"], algorithms=["HS256"],
        issuer=current_app.config["JWT_ISSUER"],
        options={"require": ["sub", "iss", "iat", "exp"]},
    )


def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


def install_auth(app):
    app.jinja_env.globals["csrf_token"] = csrf_token

    @app.before_request
    def authenticate_request():
        g.user = None
        g.identity = None
        authorization = request.headers.get("Authorization", "")
        g.bearer_auth = authorization.startswith("Bearer ")
        token = authorization[7:].strip() if g.bearer_auth else request.cookies.get(AUTH_COOKIE)
        # Static files and health checks remain usable independently of sign-in.
        if token and not request.path.startswith(("/__frontend_assets/", "/static/", "/health")):
            try:
                identity = _verify_token(token)
            except jwt.InvalidTokenError:
                identity = None
            if identity:
                with get_engine().connect() as connection:
                    user = connection.execute(
                        select(users.c.id, users.c.email).where(users.c.id == identity["sub"])
                    ).mappings().first()
                if user:
                    g.user = dict(user)
                    g.identity = identity
        if request.method in {"POST", "PUT", "PATCH", "DELETE"} and not (g.bearer_auth and g.user):
            if request.path.startswith("/api/") and not g.user:
                return jsonify(error="AUTHENTICATION_REQUIRED", message="Please sign in to continue."), 401
            submitted = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token", "")
            expected = session.get("csrf_token", "")
            if not expected or not isinstance(submitted, str) or not hmac.compare_digest(submitted.encode('utf-8'), expected.encode('utf-8')):
                return jsonify(error="INVALID_CSRF", message="Your session expired. Refresh the page and try again."), 400


def require_auth(handler):
    @wraps(handler)
    def wrapped(*args, **kwargs):
        if not g.user:
            if request.path.startswith("/api/"):
                return jsonify(error="AUTHENTICATION_REQUIRED", message="Please sign in to continue."), 401
            return redirect("/login")
        return handler(*args, **kwargs)
    return wrapped


def load_optional_auth(handler):
    return handler


def sign_in_response(user_id):
    session.clear()
    csrf_token()
    response = redirect("/", code=303)
    response.set_cookie(
        AUTH_COOKIE, issue_token(user_id), max_age=TOKEN_SECONDS,
        httponly=True, secure=current_app.config["SESSION_COOKIE_SECURE"],
        samesite="Lax", path="/",
    )
    return response
