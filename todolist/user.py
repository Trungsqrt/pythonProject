from flask import Blueprint

user = Blueprint("user", __name__)

#set address route of pages
@user.route("/login")
def login():
   return "Login Page"

@user.route("/logout")
def logout():
   return "Logout Page"

@user.route("/register")
def register():
   return "Register Page"