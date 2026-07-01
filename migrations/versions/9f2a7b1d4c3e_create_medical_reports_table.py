"""Create medical reports table

Revision ID: 9f2a7b1d4c3e
Revises: 37be95f6ec02
Create Date: 2026-07-01 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "9f2a7b1d4c3e"
down_revision = "37be95f6ec02"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "medical_reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("appointment_id", sa.Integer(), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("s3_key", sa.String(length=500), nullable=False),
        sa.Column("upload_date", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["appointment_id"], ["appointments.id"]),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade():
    op.drop_table("medical_reports")
