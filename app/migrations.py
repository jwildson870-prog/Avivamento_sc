"""Small, idempotent schema migrations for existing installations.

The project uses db.create_all() for first-time setup, but create_all() does
not add columns to tables that already exist. These migrations keep existing
Neon/PostgreSQL data intact while bringing older installations up to date.
"""

from sqlalchemy import inspect, text

from .models import db


def migrate_existing_schema():
    """Add missing columns to existing tables without dropping data."""
    inspector = inspect(db.engine)
    tables = set(inspector.get_table_names())

    # The Pastor model gained a teaching field after the initial deployment.
    # If the table already exists on Neon, db.create_all() will not add it.
    if "pastor" in tables:
        columns = {column["name"] for column in inspector.get_columns("pastor")}
        if "teaching" not in columns:
            dialect = db.engine.dialect.name
            if dialect == "postgresql":
                statement = text(
                    "ALTER TABLE pastor ADD COLUMN IF NOT EXISTS teaching TEXT"
                )
            else:
                # SQLite does not support ADD COLUMN IF NOT EXISTS.
                statement = text("ALTER TABLE pastor ADD COLUMN teaching TEXT")

            with db.engine.begin() as connection:
                connection.execute(statement)
