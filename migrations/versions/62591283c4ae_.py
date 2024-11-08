"""empty message

Revision ID: 62591283c4ae
Revises: 0289fe0309e6
Create Date: 2024-10-30 00:33:23.041834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62591283c4ae'
down_revision = '0289fe0309e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table('instagram_page', schema=None) as batch_op:
        batch_op.add_column(sa.Column('follows', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('followers', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('last_updated', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('instagram_page', schema=None) as batch_op:
        batch_op.drop_column('last_updated')
        batch_op.drop_column('followers')
        batch_op.drop_column('follows')
    # ### end Alembic commands ###
