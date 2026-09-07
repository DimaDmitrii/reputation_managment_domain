from alembic import op
import sqlalchemy as sa


revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "media",
        sa.Column(
            "preview_key",
            sa.String(length=512),
            nullable=True,
        ),
    )

    op.add_column(
        "media",
        sa.Column(
            "medium_key",
            sa.String(length=512),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column(
        "media",
        "medium_key",
    )

    op.drop_column(
        "media",
        "preview_key",
    )
