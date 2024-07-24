from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        #Get data from form
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Success!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.index"))
            else:
                flash("Incorrect password.", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':

        # Get data from registration
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        user = User.query.filter_by(email=email).first()

        # Error checking for email
        if not email:
            flash("Must provide an email.", category="error")
            return redirect(url_for("auth.register"))

        elif user:
            flash("Email already exists.", category="error")
            return redirect(url_for("auth.register"))

        # Error checking for name
        elif not name:
            flash("Must provide name.", category="error")
            return redirect(url_for("auth.register"))

        elif len(name) > 20:
            flash("Name must less than 20 characters in length.", category="error")
            return redirect(url_for("auth.register"))

        # Error checking for password
        elif not password:
            flash("Must provide password.", category="error")
            return redirect(url_for("auth.register"))

        elif len(password) < 6:
            flash("Password must be at least 6 characters in length.", category="error")
            return redirect(url_for("auth.register"))

        # Error checking for confirmation
        elif not confirmation:
            flash("Must confirm password.", category="error")
            return redirect(url_for("auth.register"))

        # Check if password and confirmation match
        elif password != confirmation:
            flash("Passwords do not match.", category="error")
            return redirect(url_for("auth.register"))

        # If all fields satisfied, register user
        else:
            user = User(email=email, name=name, password=generate_password_hash(password, method="scrypt"))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)

            flash("Success!", category="success")
            return redirect(url_for("views.index"))

    else:
        return render_template("register.html", user=current_user)
