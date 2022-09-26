import json
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .model import Note

view = Blueprint("view", __name__)

@view.route("/", methods=["GET", "POST"])
@login_required
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


# @view.route("/edit-note", methods=["POST"])
# def edit_note():
#    if request.method == "POST":
#       note = request.body.get("edited-note")

#       if len(note) < 1:
#          flash("Failed! Note is too short!")
#       else:
#          edited_note = Note(data=note, user_id=current_user.id)
#          # db.session.add(edited_note)
#          db.session.commit()
#          flash("Edit note successfully!")

#    return render_template("index.html", user=current_user)


@view.route("/delete-note", methods=["POST"])
def delete_note():
   if request.method == "POST":
      body_data = json.loads(request.data)

      note_id = body_data['note_id']
      note = Note.query.get(note_id)

      if note:
         if note.user_id == current_user.id:
            try: 
               db.session.delete(note)
               db.session.commit()
               flash("Delete note successfully!")
               return jsonify({ "status": "sucessfully" })
            except:
               flash("Delete note failed!")
               return jsonify({ "status": "failed" })
      else:
         flash("Delete note failed!")
         return jsonify({ "status": "failed" })