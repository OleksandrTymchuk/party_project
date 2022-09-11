"""005_add_inv_status_to_user_event

Revision ID: 005_add_inv_status_to_user_event
Revises: 004_add_creator_id_to_event
Create Date: 2022-09-11 10:35:48.604183

"""
from sqlalchemy.dialects import postgresql
from alembic import op
import sqlalchemy as sa

from core.models.user_event import InvitationStatus

revision = '005_add_inv_status_to_user_event'
down_revision = '004_add_creator_id_to_event'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint('event_creator_id_fkey', 'event', type_='foreignkey')
    inv_status = postgresql.ENUM(InvitationStatus, name="invitation_status")
    inv_status.create(op.get_bind(), checkfirst=True)
    op.add_column('user_event', sa.Column('invitation_status',  inv_status))


def downgrade() -> None:
    inv_status = postgresql.ENUM(InvitationStatus, name="invitation_status")
    inv_status.drop(op.get_bind())
