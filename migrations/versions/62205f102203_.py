"""empty message

Revision ID: 62205f102203
Revises: da3251c47d16
Create Date: 2020-09-14 10:43:09.535357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62205f102203'
down_revision = 'da3251c47d16'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('song_post', sa.Column('bpm', sa.Integer(), nullable=True))
    op.add_column('song_post', sa.Column('key', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('song_post', 'key')
    op.drop_column('song_post', 'bpm')
    # ### end Alembic commands ###
