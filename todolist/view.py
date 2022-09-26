from curses import flash
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
from .model import Note

view = Blueprint("view", __name__)

@view.route("/", methods=["GET", "POST"])
def home():
   if request.method == "POST":
      note = request.form.get("note")

      if len(note) < 1:
         flash("Failed! Note is too short!")
      else:
         new_note = Note(data=note, user_id=current_user.id)
         db.session.add(new_note)
         db.session.commit()
         flash("Add note successfully!")

   return render_template("index.html", user=current_user)