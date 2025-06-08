
import sqlalchemy as sa

def id_column():
    return sa.Column(
        "id",
        sa.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

def county_id_column():
    return sa.Column(
        "county_id",
        sa.Integer,
        sa.ForeignKey("counties.id"),
        nullable=False
    )

def municipality_id_column():
    return sa.Column(
        "municipality_id",
        sa.Integer,
        sa.ForeignKey("municipalities.id"),
        nullable=False
    )

def standard_columns():
    return [
        id_column(),
        created_at_column(),
        updated_at_column()
    ]

def created_at_column():
    return sa.Column(
        "created_at",
        sa.DateTime,
        default=sa.func.now(),
        server_default=sa.func.now(),
        nullable=False
    )

def updated_at_column():
    return sa.Column(
        "updated_at",
        sa.DateTime,
        default=sa.func.now(),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        server_onupdate=sa.func.now(),
        nullable=False
    )

def report_id_column():
    return sa.Column(
        "report_id",
        sa.Integer,
        sa.ForeignKey("annual_reports.id"),
        nullable=False
    )