"""empty message

Revision ID: f5a78dbc58bc
Revises: 
Create Date: 2023-02-10 15:09:15.734275

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "f5a78dbc58bc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("username", sa.VARCHAR(length=30), nullable=False),
        sa.Column("password", sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__user")),
    )
    op.create_index(op.f("ix__user__username"), "user", ["username"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix__user__username"), table_name="user")
    op.drop_table("user")
