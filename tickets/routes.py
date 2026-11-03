# tickets/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from auth.decorators import login_required, role_required
from auth.service import get_current_user
from auth.roles import ROLE_ADMIN, ROLE_AGENT

from . import repository as repo
from . import service as svc

# Point the blueprint at the project-level /templates folder
# (i.e., /home/vicki888blue/templates on PythonAnywhere)
tickets_bp = Blueprint(
    "tickets",
    __name__,
    template_folder="../templates"
)

# LIST: GET /tickets   (works with url_for("tickets.list"))
@tickets_bp.get("/", endpoint="list")
@login_required
def list_tickets():
    rows = repo.list_tickets()
    return render_template("tickets_list.html", rows=rows, user=get_current_user())

# NEW FORM: GET /tickets/new  (Admin + Agent)
@tickets_bp.get("/new")
@login_required
@role_required(ROLE_ADMIN, ROLE_AGENT)
def new_form():
    return render_template("tickets_new.html", user=get_current_user())

# CREATE: POST /tickets  (Admin + Agent)
@tickets_bp.post("/")
@login_required
@role_required(ROLE_ADMIN, ROLE_AGENT)
def create():
    user = get_current_user()

    # Validate form input
    errors, data = svc.validate_new(request.form, user["username"])
    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("tickets.new_form"))

    try:
        repo.create_ticket(data)  # raises IntegrityError on unique violations
    except IntegrityError:
        flash(f"Ticket '{data['Ticket']}' already exists. Choose a different Ticket ID.", "error")
        return redirect(url_for("tickets.new_form"))

    flash("Ticket created.", "success")
    return redirect(url_for("tickets.list"))

# DETAIL: GET /tickets/<ticket>  (logged-in)
@tickets_bp.get("/<ticket>")
@login_required
def detail(ticket):
    row = repo.get_ticket(ticket)
    if not row:
        return ("Not found", 404)
    return render_template("ticket_detail.html", row=row, user=get_current_user())

# EDIT FORM: GET /tickets/<ticket>/edit  (Admin + Agent)
@tickets_bp.get("/<ticket>/edit")
@login_required
@role_required(ROLE_ADMIN, ROLE_AGENT)
def edit_form(ticket):
    row = repo.get_ticket(ticket)
    if not row:
        return ("Not found", 404)
    return render_template("tickets_edit.html", row=row, user=get_current_user())

# UPDATE: POST /tickets/<ticket>/edi  (Admin + Agent)
@tickets_bp.post("/<ticket>/edit")
@login_required
@role_required(ROLE_ADMIN, ROLE_AGENT)
def update(ticket):
    user = get_current_user()

    errors, data = svc.validate_update(request.form, user["username"])
    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("tickets.edit_form", ticket=ticket))

    updated = repo.update_ticket(ticket, data)
    flash("Ticket updated." if updated else "Ticket not found.", "success" if updated else "error")
    return redirect(url_for("tickets.detail", ticket=ticket))

# CLOSE: POST /tickets/<ticket>/close  (Admin + Agent)
@tickets_bp.post("/<ticket>/close")
@login_required
@role_required(ROLE_ADMIN, ROLE_AGENT)
def close(ticket):
    updated = repo.close_ticket(ticket)
    flash("Ticket closed." if updated else "Ticket not found.", "success" if updated else "error")
    return redirect(url_for("tickets.detail", ticket=ticket))

# DELETE: POST /tickets/<ticket>/delete  (Admin + Agent)
@tickets_bp.post("/<ticket>/delete")
@login_required
@role_required(ROLE_ADMIN, ROLE_AGENT)
def delete(ticket):
    deleted = repo.delete_ticket(ticket)
    flash("Ticket deleted." if deleted else "Ticket not found.", "success" if deleted else "error")
    return redirect(url_for("tickets.list"))


