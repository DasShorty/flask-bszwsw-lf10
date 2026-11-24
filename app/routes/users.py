from flask import Blueprint, request, redirect, url_for, render_template

from ..extensions import db
from ..models import User

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/")
def list_users():
    users = User.query.order_by(User.name).all()
    return render_template("users/list.html", users=users)

@bp.route("/new", methods=["POST"])
def create_user():
    db.session.add(User(name=request.form["name"], email=request.form["email"]))
    db.session.commit()
    return redirect(url_for("users.list_users"))
