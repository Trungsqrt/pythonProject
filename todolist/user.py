from flask import Blueprint, render_template

user = Blueprint("user", __name__)

#set address route of pages
@user.route("/login")
def login():
   return render_template("login.html")

@user.route("/logout")
def logout():
   return render_template("logout.html")

@user.route("/register")
def register():
   return render_template("register.html")