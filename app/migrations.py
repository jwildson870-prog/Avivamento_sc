"""Idempotent database schema migrations for the Avivamento app.

The application historically used ``db.create_all()`` only. That creates tables
that are missing, but it does not update tables that already exist with columns
added by newer versions. This module bridges that gap without deleting data.
"""

from sqlalchemy import inspect, text

from .models import db


# PostgreSQL types used when a column needs to be added to an existing table.
# The values are intentionally simple and portable enough for the SQLite dev DB.
COLUMN_TYPES = {
    "user": {
        "username": "VARCHAR(80)",
        "email": "VARCHAR(160)",
        "password_hash": "VARCHAR(255)",
        "role": "VARCHAR(20)",
        "photo": "VARCHAR(255)",
        "created_at": "TIMESTAMP",
    },
    "site_content": {
        "key": "VARCHAR(80)",
        "title": "VARCHAR(180)",
        "body": "TEXT",
        "updated_at": "TIMESTAMP",
    },
    "pastor": {
        "name": "VARCHAR(160)",
        "role": "VARCHAR(120)",
        "bio": "TEXT",
        "photo": "VARCHAR(255)",
        "created_at": "TIMESTAMP",
    },
    "notice": {
        "title": "VARCHAR(180)",
        "body": "TEXT",
        "image": "VARCHAR(255)",
        "created_at": "TIMESTAMP",
    },
    "announcement": {
        "title": "VARCHAR(180)",
        "body": "TEXT",
        "media": "VARCHAR(255)",
        "media_type": "VARCHAR(20)",
        "created_at": "TIMESTAMP",
    },
}


def _table_columns(inspector, table_name):
    return {column["name"] for column in inspector.get_columns(table_name)}


def _add_missing_columns(connection, table_name, model_table):
    inspector = inspect(connection)
    if table_name not in inspector.get_table_names():
        return

    existing = _table_columns(inspector, table_name)
    expected = COLUMN_TYPES.get(table_name, {})

    for column_name, column_type in expected.items():
        if column_name in existing:
            continue

        # New columns are nullable so an existing production table can be
        # migrated without failing because it already contains rows.
        statement = f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" {column_type}'
        connection.execute(text(statement))


def run_migrations():
    """Create missing tables and add missing columns without destroying data."""
    with db.engine.begin() as connection:
        # create_all handles tables that do not exist at all (including notice).
        db.metadata.create_all(bind=connection)

        inspector = inspect(connection)
        for table_name, model_table in db.metadata.tables.items():
            _add_missing_columns(connection, table_name, model_table)

        # Re-inspect after ALTER TABLE operations and ensure every expected
        # application table exists. This is intentionally idempotent.
        inspect(connection)
