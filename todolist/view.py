from flask import Blueprint

view = Blueprint("view", __name__)

#set address route of pages
@view.route("/")
def home():
   return "HomePage"