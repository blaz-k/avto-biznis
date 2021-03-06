from flask import render_template, request, redirect, url_for, make_response
from hashlib import sha256
import uuid

from models.user import User
from models.settings import db


def login():
    if request.method == "GET":
        return render_template("/auth/login.html")

    elif request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        password_hash = sha256(password.encode("utf-8")).hexdigest()

        existing_user = db.query(User).filter_by(username=username, password=password_hash).first()

        if existing_user:
            session_token = str(uuid.uuid4())
            existing_user.session_token = session_token
            existing_user.save()

            response = make_response(redirect(url_for("dashboard.dashboard")))
            response.set_cookie("session", session_token)
            return response
        else:
            return render_template("error-login.html")
    return redirect(url_for("dashboard.dashboard"))


def logout():
    session_cookie = request.cookies.get("session")
    user = db.query(User).filter_by(session_token=session_cookie).first()
    user.session_token = ""
    user.save()

    return redirect(url_for("auth.login"))


def registration():
    if request.method == "GET":
        return render_template("/auth/registration.html")

    elif request.method == "POST":

        username = request.form.get("username")
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        country = request.form.get("country")
        postal_code = request.form.get("postal-code")
        email = request.form.get("user-email")
        phone_number = request.form.get("telephone")
        password = request.form.get("password")
        repeat = request.form.get("repeat")

        existing_user = db.query(User).filter_by(username=username).first()

        if existing_user:
            return "ERROR: This username already exist! You need to choose something else."
        else:

            if password == repeat:

                password_hash = sha256(password.encode("utf-8")).hexdigest()
                new_user = User(username=username, first_name=first_name, last_name=last_name,
                                country=country, postal_code=postal_code, email=email,
                                phone_number=phone_number, password=password_hash)
                new_user.save()

                return render_template("successful.html")
            else:
                return render_template("passwords-not-match.html")

    return redirect(url_for("public.home"))

