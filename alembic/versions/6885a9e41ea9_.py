"""init

Revision ID: 6885a9e41ea9
Revises:
Create Date: 2024-08-27 15:17:11.907172

"""

from collections.abc import Sequence

import advanced_alchemy
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6885a9e41ea9"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "source",
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("feed_url", sa.String(), nullable=False),
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("created_at", advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column("updated_at", advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_source")),
    )
    op.create_table(
        "user",
        sa.Column("tg_id", sa.BigInteger(), nullable=False),
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("created_at", advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column("updated_at", advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user")),
        sa.UniqueConstraint("tg_id", name=op.f("uq_user_tg_id")),
    )
    op.create_table(
        "news",
        sa.Column("source_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("internal_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("pub_date", advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("created_at", advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column("updated_at", advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["source_id"], ["source.id"], name=op.f("fk_news_source_id_source")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_news")),
    )
    op.create_index(op.f("ix_news_internal_id"), "news", ["internal_id"], unique=False)
    op.create_index(op.f("ix_news_source_id"), "news", ["source_id"], unique=False)
    op.create_table(
        "user_source",
        sa.Column("user_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=True),
        sa.Column("source_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=True),
        sa.ForeignKeyConstraint(["source_id"], ["source.id"], name=op.f("fk_user_source_source_id_source")),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name=op.f("fk_user_source_user_id_user")),
    )


def downgrade() -> None:
    op.drop_table("user_source")
    op.drop_index(op.f("ix_news_source_id"), table_name="news")
    op.drop_index(op.f("ix_news_internal_id"), table_name="news")
    op.drop_table("news")
    op.drop_table("user")
    op.drop_table("source")
