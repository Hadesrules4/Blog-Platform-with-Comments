from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from .extensions import bcrypt, db
from .models import User
from .utils import validate_credentials

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        errors = validate_credentials(username, email, password)
        if User.query.filter_by(username=username).first():
            errors.append("Username is already registered.")
        if User.query.filter_by(email=email).first():
            errors.append("Email is already registered.")
        if errors:
            for error in errors: flash(error, "danger")
            return render_template("register.html")
        user = User(username=username, email=email, password_hash=bcrypt.generate_password_hash(password).decode("utf-8"))
        db.session.add(user); db.session.commit()
        flash("Account created successfully. You can now log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    if request.method == "POST":
        identity = request.form.get("identity", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter((User.email == identity.lower()) | (User.username == identity)).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=False)
            flash("Welcome back!", "success")
            next_url = request.args.get("next", "")
            if next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)
            return redirect(url_for("main.home"))
        flash("Invalid username/email or password.", "danger")
    return render_template("login.html")

@auth_bp.post("/logout")
def logout():
    if current_user.is_authenticated: logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))
