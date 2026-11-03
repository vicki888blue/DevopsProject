# tickets/service.py
from datetime import datetime

ALLOWED_PRIORITIES = {"low", "medium", "high", "urgent"}
ALLOWED_STATUSES = {"Open", "In Prog", "Closed"}  # match your form options

def _clean_str(v):
    return v.strip() if isinstance(v, str) else v

def _coerce_int(v):
    if v is None:
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None

def validate_new(form, created_by: str):
    """
    Validate incoming form for creating a ticket.
    Returns: (errors, data)
    Keys returned are TitleCase to match your repo/DB style.
    """
    errors = []

    ticket      = _clean_str(form.get("Ticket") or form.get("ticket") or "")
    title       = _clean_str(form.get("Title") or form.get("title") or "")
    description = _clean_str(form.get("Description") or form.get("description") or "")
    status      = _clean_str(form.get("Status") or form.get("status") or "Open")
    status_id   = _coerce_int(form.get("StatusID") or form.get("status_id"))
    priority_id = _coerce_int(form.get("PriorityID") or form.get("priority_id"))

    if not ticket:
        errors.append("Ticket ID is required.")
    if not title:
        errors.append("Title is required.")
    if status not in ALLOWED_STATUSES:
        errors.append(f"Status must be one of: {', '.join(ALLOWED_STATUSES)}.")
    if status_id is None or status_id < 1:
        errors.append("StatusID must be a positive integer.")
    if priority_id is None or priority_id < 1:
        errors.append("PriorityID must be a positive integer.")
    if title and len(title) > 255:
        errors.append("Title must be 255 characters or fewer.")

    data = {
        "Ticket": ticket,
        "Title": title,
        "Description": description or "",
        "Status": status,
        "StatusID": status_id,
        "PriorityID": priority_id,
        "CreatedBy": created_by,
        "CreatedAt": datetime.utcnow().isoformat(timespec="seconds"),
    }
    return errors, data

def validate_update(form, username: str):
    """
    Validate update form fields. Returns only fields provided.
    """
    errors = []
    data = {}

    raw_title       = form.get("Title",       form.get("title"))
    raw_description = form.get("Description", form.get("description"))
    raw_status      = form.get("Status",      form.get("status"))
    raw_status_id   = form.get("StatusID",    form.get("status_id"))
    raw_priority_id = form.get("PriorityID",  form.get("priority_id"))
    raw_assignee    = form.get("Assignee",    form.get("assignee"))

    if raw_title is not None:
        title = _clean_str(raw_title) or ""
        if not title:
            errors.append("Title cannot be empty.")
        elif len(title) > 255:
            errors.append("Title must be 255 characters or fewer.")
        else:
            data["Title"] = title

    if raw_description is not None:
        data["Description"] = _clean_str(raw_description) or ""

    if raw_status is not None:
        status = _clean_str(raw_status) or ""
        if not status:
            errors.append("Status is required when provided.")
        elif status not in ALLOWED_STATUSES:
            errors.append(f"Status must be one of: {', '.join(ALLOWED_STATUSES)}.")
        else:
            data["Status"] = status

    if raw_status_id is not None:
        status_id = _coerce_int(raw_status_id)
        if status_id is None or status_id < 1:
            errors.append("StatusID must be a positive integer.")
        else:
            data["StatusID"] = status_id

    if raw_priority_id is not None:
        priority_id = _coerce_int(raw_priority_id)
        if priority_id is None or priority_id < 1:
            errors.append("PriorityID must be a positive integer.")
        else:
            data["PriorityID"] = priority_id

    if raw_assignee is not None:
        data["Assignee"] = _clean_str(raw_assignee) or ""

    # audit fields (if your schema supports them)
    data["UpdatedBy"] = username
    data["UpdatedAt"] = datetime.utcnow().isoformat(timespec="seconds")

    non_audit = {k: v for k, v in data.items() if k not in {"UpdatedBy", "UpdatedAt"}}
    if not non_audit:
        errors.append("No fields provided to update.")

    return errors, data