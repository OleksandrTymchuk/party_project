"""006_add_telegram_token

Revision ID: 006_add_telegram_token
Revises: 005_add_inv_status_to_user_event
Create Date: 2022-09-13 00:19:53.078470

"""
from alembic import op
import sqlalchemy as sa


revision = '006_add_telegram_token'
down_revision = '005_add_inv_status_to_user_event'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'user',
        sa.Column('telegram_token', sa.String(), nullable=True, unique=True)
    )


def downgrade() -> None:
    op.drop_column('user', 'telegram_token')
