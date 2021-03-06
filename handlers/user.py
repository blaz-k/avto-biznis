from flask import render_template, request, redirect, url_for
from models.user import User
from models.settings import db
from hashlib import sha256


def edit_profile():
    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()

        if not user:
            return render_template("error.html")

    else:
        return render_template("error.html")

    if request.method == "GET":
        return render_template("dashboard-edit-profile.html", user=user)

    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        country = request.form.get("country")
        postal_code = request.form.get("postal-code")
        email = request.form.get("user-email")
        telephone = request.form.get("telephone")
        password = request.form.get("password")
        repeat = request.form.get("repeat")

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.country = country
        user.postal_code = postal_code
        user.email = email
        user.telephone = telephone
        user.password = sha256(password.encode("utf-8")).hexdigest()
        user.repeat = repeat
        user.save()

        return redirect(url_for("dashboard.dashboard"))
