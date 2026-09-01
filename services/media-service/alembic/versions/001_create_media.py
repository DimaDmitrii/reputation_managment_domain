from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "media",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "original_filename",
            sa.String(length=255),
            nullable=False,
        ),

        sa.Column(
            "object_key",
            sa.String(length=512),
            nullable=False,
        ),

        sa.Column(
            "content_type",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "expected_size",
            sa.BigInteger(),
            nullable=False,
        ),

        sa.Column(
            "actual_size",
            sa.BigInteger(),
            nullable=True,
        ),

        sa.Column(
            "status",
            sa.String(length=32),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("object_key"),
    )

    op.create_index(
        "ix_media_status",
        "media",
        ["status"],
    )


def downgrade():
    op.drop_index(
        "ix_media_status",
        table_name="media",
    )

    op.drop_table("media")
