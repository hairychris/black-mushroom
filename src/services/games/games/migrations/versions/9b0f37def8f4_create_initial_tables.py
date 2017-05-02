"""create initial tables

Revision ID: 9b0f37def8f4
Revises:
Create Date: 2017-04-26 14:53:28.295249

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils as sau


# revision identifiers, used by Alembic.
revision = '9b0f37def8f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'games',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('deck_id', sa.Integer),
        sa.Column('player_id', sa.Integer),
        sa.Column('player_hand', sau.ScalarListType(), default=[]),
        sa.Column('player_score', sa.Integer, default=0),
        sa.Column('player_ace_high', sa.Boolean, default=False),
        sa.Column('dealer_hand', sau.ScalarListType(), default=[]),
        sa.Column('dealer_hand_hidden', sau.ScalarListType(), default=[]),
        sa.Column('dealer_score', sa.Integer, default=0),
        sa.Column('dealer_ace_high', sa.Boolean, default=False),
        sa.Column('dealer_ace_high_hidden', sa.Boolean, default=False),
        sa.Column('status', sa.Integer, default=0),
    )


def downgrade():
    op.drop_table('games')
