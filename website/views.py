from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        note = request.form.get("note")

        # Error checking for note
        if len(note) < 1:
            flash("Empty note.", category="error")
            return redirect(url_for("views.index"))

        # Add note
        else:
            new_note = Note(text=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('views.index'))

    return render_template('index.html', user=current_user)

@views.route("/<int:id>/edit/", methods=["GET", "POST"])
@login_required
def edit(id):

    note = Note.query.get(id)

    if request.method == "POST":

        edited_note = request.form.get("note")

        # Edit note
        if note:
            if note.user_id == current_user.id:
                note.text = edited_note
                db.session.commit()

        return redirect(url_for("views.index"))

    else:
        return render_template("edit.html", user=current_user, note=note)


@views.route("/<int:id>/delete/", methods=["GET"])
@login_required
def delete(id):

    note = Note.query.get(id)

    # Delete note
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return redirect(url_for("views.index"))
