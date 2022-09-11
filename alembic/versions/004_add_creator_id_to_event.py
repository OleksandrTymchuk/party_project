"""004_add_creator_id_to_event

Revision ID: 004_add_creator_id_to_event
Revises: 003_make_event_desc_nullable
Create Date: 2022-09-11 10:06:36.084232

"""
from alembic import op
import sqlalchemy as sa


revision = '004_add_creator_id_to_event'
down_revision = '003_make_event_desc_nullable'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('event', sa.Column('creator_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False))


def downgrade() -> None:
    op.drop_column('event', 'creator_id')
