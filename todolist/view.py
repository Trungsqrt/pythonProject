from flask import Blueprint, render_template
from flask_login import login_required, current_user
view = Blueprint("view", __name__)

#set address route of pages
@view.route("/")
def home():
   return render_template("index.html", user = current_user)