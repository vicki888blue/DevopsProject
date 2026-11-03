from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session
)
from .service import register_user, authenticate
from .roles import ROLE_USER
import re

# IMPORTANT:
# We point the blueprint to the main /templates folder.
# Your templates live in /home/vicki888blue/templates
auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="../templates"
)


# ------------------------
# PASSWORD VALIDATION
# ------------------------

def validate_password(password):
    """
    Password requirements:
    - Minimum 12 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """

    if len(password) < 12:
        return "Password must be at least 12 characters long."

    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return "Password must contain at least one number."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character."

    return None


# ------------------------
# REGISTER (GET + POST)
# ------------------------

@auth_bp.get("/register")
def register_form():
    return render_template("register.html")


@auth_bp.post("/register")
def register_submit():
    username = (request.form.get("username") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    confirm = request.form.get("confirm") or ""

    # Basic validations
    if not username:
        flash("Username is required.", "error")
        return redirect(url_for("auth.register_form"))

    if not email:
        flash("Email address is required.", "error")
        return redirect(url_for("auth.register_form"))

    if not password or not confirm:
        flash("Password and confirmation are required.", "error")
        return redirect(url_for("auth.register_form"))

    if password != confirm:
        flash("Passwords do not match.", "error")
        return redirect(url_for("auth.register_form"))

    # Password strength validation
    validation_error = validate_password(password)

    if validation_error:
        flash(validation_error, "error")
        return redirect(url_for("auth.register_form"))

    try:
        register_user(
            username=username,
            email=email,
            password=password,
            role_id=ROLE_USER
        )

        flash(
            "Registration successful! Please log in.",
            "success"
        )

        return redirect(url_for("auth.login_form"))

    except Exception:
        flash(
            "Registration error. Try a different username or email address.",
            "error"
        )

        return redirect(url_for("auth.register_form"))


# ------------------------
# LOGIN (GET + POST)
# ------------------------

@auth_bp.get("/login")
def login_form():
    return render_template("login.html")


@auth_bp.post("/login")
def login_submit():
    username_or_email = (
        request.form.get("username_or_email") or ""
    ).strip()

    password = request.form.get("password") or ""

    if not username_or_email or not password:
        flash(
            "Please enter your login details.",
            "error"
        )

        return redirect(url_for("auth.login_form"))

    user = authenticate(
        username_or_email,
        password
    )

    if not user:
        flash(
            "Invalid username/email or password.",
            "error"
        )

        return redirect(url_for("auth.login_form"))

    # Store session information
    session.clear()
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["role_id"] = user["role_id"]

    if "role_name" in user and user["role_name"]:
        session["role_name"] = user["role_name"]

    flash(
        f"Welcome, {user['username']}!",
        "success"
    )

    return redirect(url_for("tickets.list"))


# ------------------------
# LOGOUT
# ------------------------

@auth_bp.post("/logout")
def logout():
    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(url_for("auth.login_form"))