from __future__ import annotations

from typing import Any, Dict, List, Optional
from sqlalchemy import text
from db import connect, transaction


# -------- Read operations --------

def list_tickets() -> List[Dict[str, Any]]:
    """
    Returns tickets with the columns that actually exist in your current schema.
    """
    sql = text("""
        SELECT
            Ticket,
            Status,
            CreatedBy,
            PriorityID,
            StatusID
        FROM Tickets
        ORDER BY Ticket ASC
    """)
    with connect() as conn:
        return [dict(r) for r in conn.execute(sql).mappings().all()]


def get_ticket(ticket_id: str) -> Optional[Dict[str, Any]]:
    sql = text("""
        SELECT
            Ticket,
            Status,
            CreatedBy,
            PriorityID,
            StatusID
        FROM Tickets
        WHERE Ticket = :t
    """)
    with connect() as conn:
        row = conn.execute(sql, {"t": ticket_id}).mappings().first()
        return dict(row) if row else None


def exists_ticket(ticket_id: str) -> bool:
    sql = text("SELECT 1 FROM Tickets WHERE Ticket = :t LIMIT 1")
    with connect() as conn:
        return conn.execute(sql, {"t": ticket_id}).first() is not None




def create_ticket(data: Dict[str, Any]) -> None:
    """
    Insert using only existing columns.
    Expects keys: Ticket, Status, CreatedBy, PriorityID, StatusID
    (Extra keys in `data` are ignored.)
    """
    sql = text("""
        INSERT INTO Tickets (Ticket, Status, CreatedBy, PriorityID, StatusID)
        VALUES (:Ticket, :Status, :CreatedBy, :PriorityID, :StatusID)
    """)
    params = {
        "Ticket":     data["Ticket"],
        "Status":     data["Status"],
        "CreatedBy":  data["CreatedBy"],
        "PriorityID": data["PriorityID"],
        "StatusID":   data["StatusID"],
    }
    with transaction() as conn:
        conn.execute(sql, params)
    # Let IntegrityError bubble to the route if a duplicate key occurs.


def update_ticket(ticket_id: str, data: Dict[str, Any]) -> bool:
    """
    Partial update for existing columns only.
    Allowed fields: Status, PriorityID, StatusID
    (We do NOT update CreatedBy when editing.)
    """
    allowed = {"Status", "PriorityID", "StatusID"}

    sets: List[str] = []
    params: Dict[str, Any] = {"t": ticket_id}
    for k in allowed:
        if k in data:
            sets.append(f"{k} = :{k}")
            params[k] = data[k]

    if not sets:
        return False

    sql = text(f"UPDATE Tickets SET {', '.join(sets)} WHERE Ticket = :t")
    with transaction() as conn:
        res = conn.execute(sql, params)
        return res.rowcount > 0


def close_ticket(ticket_id: str) -> bool:
    sql = text("UPDATE Tickets SET Status = 'Closed' WHERE Ticket = :t")
    with transaction() as conn:
        res = conn.execute(sql, {"t": ticket_id})
        return res.rowcount > 0


def delete_ticket(ticket_id: str) -> bool:
    sql = text("DELETE FROM Tickets WHERE Ticket = :t")
    with transaction() as conn:
        res = conn.execute(sql, {"t": ticket_id})
        return res.rowcount > 0


