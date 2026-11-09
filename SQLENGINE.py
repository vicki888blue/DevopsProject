from sqlalchemy import create_engine, text
from pathlib import Path

DB_PATH = Path(__file__).parent / "mydatabase.db"
engine = create_engine(f"sqlite:///{DB_PATH.as_posix()}", echo=True)

with engine.begin() as conn:
    # Drop the old table if it exists (destroys its data)
    conn.execute(text("DROP TABLE IF EXISTS Tickets;"))

    # ✅ Recreate with the columns your app expects
    conn.execute(text("""
        CREATE TABLE Tickets (
            Ticket      VARCHAR PRIMARY KEY,
            Status      VARCHAR,
            CreatedBy   VARCHAR,
            PriorityID  INTEGER,
            StatusID    VARCHAR
        )
    """))

    # Seed
    conn.execute(text("""
        INSERT INTO Tickets (Ticket, Status, CreatedBy, PriorityID, StatusID)
        VALUES
            ('INC-1001', 'Open',   'Victoria', 2, 'S1'),
            ('INC-1002', 'Closed', 'Damian',   1, 'S2'),
            ('INC-1003', 'In Prog','Gregor',   3, 'S1')
    """))

print("Recreated Tickets table at:", engine.url.database)

