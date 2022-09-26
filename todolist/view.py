from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .model import Note
import json 

view = Blueprint("view", __name__)

@view.route("/", methods=["GET"])
@login_required
def home():
   return render_template("index.html", user=current_user)


@view.route("/add-note", methods=["POST"])
@login_required
def add_note():
   body_data = json.loads(request.data)
   new_note = body_data['new_note']

   if len(new_note) < 1:
      flash("Failed! Note is too short!")
   else:
      try: 
         new_note_data = Note(data=new_note, user_id=current_user.id)
         db.session.add(new_note_data)
         db.session.commit()
      
         flash("Add note successfully!")
      except:
         flash("Add note failed!")

   return jsonify({})


@view.route("/edit-note", methods=["POST"])
@login_required
def edit_note():
   body_data = json.loads(request.data)

   note_id = body_data['note_id']
   note_edit_value = body_data['note_edit_value']
   note = Note.query.get(note_id)

   if note:
      if note.user_id == current_user.id:
         try: 
            note = Note.query.filter_by(id=note_id).first()
            note.data = note_edit_value
            db.session.commit()

            flash("Edit note successfully!")
         except:
            flash("Edit note failed!")
   else:
      flash("Edit note failed!")

   return jsonify({})


@view.route("/delete-note", methods=["POST"])
@login_required
def delete_note():
   body_data = json.loads(request.data)

   note_id = body_data['note_id']
   note = Note.query.get(note_id)

   if note:
      if note.user_id == current_user.id:
         try: 
            db.session.delete(note)
            db.session.commit()

            flash("Delete note successfully!")
         except:
            flash("Delete note failed!")
   else:
      flash("Delete note failed!")

   return jsonify({})

