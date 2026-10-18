"""Small email/password registration and login flow."""
import re
import uuid
from datetime import datetime, timezone

from flask import Blueprint, g, redirect, render_template, request, session
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from backend.core.auth import AUTH_COOKIE, hash_password, sign_in_response, verify_password
from backend.core.db import get_engine, users

blueprint = Blueprint("authentication", __name__)


def auth_page(mode, error=None, email="", status=200):
    return render_template(
        "features/authentication/auth_screen.html",
        mode=mode, error=error, email=email,
    ), status


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    if g.user:
        return redirect("/")
    if request.method == "GET":
        return auth_page("register")
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirmation = request.form.get("confirm_password", "")
    if len(email) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        return auth_page("register", "Enter a valid email address.", email, 400)
    if not 8 <= len(password) <= 128:
        return auth_page("register", "Use a password between 8 and 128 characters.", email, 400)
    if password != confirmation:
        return auth_page("register", "The passwords do not match.", email, 400)
    user_id = str(uuid.uuid4())
    try:
        with get_engine().begin() as connection:
            connection.execute(insert(users).values(
                id=user_id, email=email, password_hash=hash_password(password),
                created_at=datetime.now(timezone.utc).replace(tzinfo=None),
            ))
    except IntegrityError:
        return auth_page("register", "This email is already registered. Please sign in.", email, 409)
    return sign_in_response(user_id)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if g.user:
        return redirect("/")
    if request.method == "GET":
        return auth_page("login")
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    if len(email) > 254 or not 1 <= len(password) <= 128:
        return auth_page("login", "Email or password is incorrect.", email, 401)
    with get_engine().connect() as connection:
        user = connection.execute(select(users).where(users.c.email == email)).mappings().first()
    if not user or not verify_password(password, user["password_hash"]):
        return auth_page("login", "Email or password is incorrect.", email, 401)
    return sign_in_response(user["id"])


@blueprint.post("/logout")
def logout():
    session.clear()
    response = redirect("/login", code=303)
    response.delete_cookie(AUTH_COOKIE, path="/")
    return response
