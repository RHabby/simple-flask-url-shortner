"""links table

Revision ID: 804436e908d0
Revises: de484c97db97
Create Date: 2020-08-31 12:42:53.611509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '804436e908d0'
down_revision = 'de484c97db97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original_link', sa.String(length=256), nullable=True),
    sa.Column('short_link', sa.String(length=6), nullable=True),
    sa.Column('creation_time', sa.DateTime(), nullable=True),
    sa.Column('visits', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short_link')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('link')
    # ### end Alembic commands ###
