"""create initial tables

Revision ID: 58a14b87c3fc
Revises:
Create Date: 2017-04-26 14:50:26.597677

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils as sau


# revision identifiers, used by Alembic.
revision = '58a14b87c3fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'decks',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('face_down_cards', sau.ScalarListType(), default=[]),
        sa.Column('dealt_cards', sau.ScalarListType(), default=[]),
    )


def downgrade():
    op.drop_table('decks')
