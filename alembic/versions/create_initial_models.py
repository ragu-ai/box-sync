"""create datasoureces, folders,assistant folder models

Revision ID: 17adaecd2bfa
Revises:
Create Date: 2024-10-18 18:06:55.666131

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "17adaecd2bfa"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "data_sources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("external_id", sa.String(length=50), nullable=True),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("service", sa.String(length=50), nullable=False),
        sa.Column("credentials", sa.String(length=50), nullable=True),
        sa.Column("active", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "folders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("data_source_id", sa.Integer(), nullable=False),
        sa.Column("active", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["data_source_id"], ["data_sources.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "assistant_folders",
        sa.Column("assistant_id", sa.Integer(), nullable=False),
        sa.Column("folder_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["folder_id"], ["folders.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("assistant_id"),
    )


def downgrade() -> None:
    op.drop_table("assistant_folders")
    op.drop_table("folders")
    op.drop_table("data_sources")
