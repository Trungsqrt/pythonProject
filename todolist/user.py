from math import e
from re import template
from unicodedata import category
from flask import Blueprint, render_template,  request, session, flash
from flask.helpers import url_for
from sqlalchemy.sql.expression import false
from werkzeug.utils import redirect
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user,login_required, logout_user,current_user
from todolist import view
from .model import User, Note
from .import db

user = Blueprint("user", __name__)

@user.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                session.permanent = True
                login_user(user, remember=True)
                flash("Login in success!", category="success")
                return redirect(url_for("view.home"))
            else: 
                flash("Wrong password, please check again!", category="error")
        else:
            flash("User doesn't exist!", category="error")
    return render_template("login.html", user=current_user)


@user.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST": 
        email = request.form.get("email")
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user = User.query.filter_by(email=email).first()
        #validate user
        if user:
            flash("User existed!", category="error")
        elif len(email) < 4 :
            flash("Email must be greater then 3 characters.", category="error")
        elif len(password) < 7:
            flash("Password must be greater then 7 characters.", category="error")
        elif password != confirm_password:
            flash("Password doesn't match.", category="error")
        else :
            password = generate_password_hash(password, method="sha256")
            new_user = User(email, password, user_name)
            try:
                db.session.add(new_user)
                db.session.commit()
                
                flash("User create!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("view.home"))
            except:
                "error"
    return render_template("signup.html", user=current_user)


@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))