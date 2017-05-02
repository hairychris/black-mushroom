"""create initial tables

Revision ID: c8ca840a4824
Revises:
Create Date: 2017-04-26 14:53:45.267903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8ca840a4824'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'players',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(50), nullable=False),
    )


def downgrade():
    op.drop_table('players')
