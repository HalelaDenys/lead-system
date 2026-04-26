"""Added lead table

Revision ID: b05481c62599
Revises: 6569798f361d
Create Date: 2026-04-26 16:56:03.991553

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "b05481c62599"
down_revision: Union[str, Sequence[str], None] = "6569798f361d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "leads",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("name", sa.VARCHAR(length=255), nullable=False),
        sa.Column("phone", sa.VARCHAR(length=20), nullable=False),
        sa.Column("country", sa.VARCHAR(length=50), nullable=False),
        sa.Column("offer_id", sa.UUID(), nullable=False),
        sa.Column("affiliate_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["affiliate_id"],
            ["affiliates.id"],
            name=op.f("fk_leads_affiliate_id_affiliates"),
        ),
        sa.ForeignKeyConstraint(
            ["offer_id"], ["offers.id"], name=op.f("fk_leads_offer_id_offers")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_leads")),
    )
    op.create_index(
        "idx_leads_affiliate_created",
        "leads",
        ["affiliate_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "idx_leads_offer_created", "leads", ["offer_id", "created_at"], unique=False
    )


def downgrade() -> None:
    op.drop_index("idx_leads_offer_created", table_name="leads")
    op.drop_index("idx_leads_affiliate_created", table_name="leads")
    op.drop_table("leads")
