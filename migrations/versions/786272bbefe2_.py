"""empty message

Revision ID: 786272bbefe2
Revises: 
Create Date: 2024-10-27 23:36:05.053469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '786272bbefe2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('instagram_page', schema=None) as batch_op:
        # batch_op.drop_constraint('shop_id', type_='foreignkey')
        batch_op.drop_column('shop_id')

    with op.batch_alter_table('shop', schema=None) as batch_op:
        batch_op.add_column(sa.Column('instagram_page_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('instagram_page_id', 'instagram_page', ['instagram_page_id'], ['id'])
        batch_op.drop_column('instagram_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shop', schema=None) as batch_op:
        batch_op.add_column(sa.Column('instagram_id', sa.VARCHAR(length=80), nullable=True))
        batch_op.drop_constraint('instagram_page_id', type_='foreignkey')
        batch_op.drop_column('instagram_page_id')

    with op.batch_alter_table('instagram_page', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shop_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('shop_id', 'shop', ['shop_id'], ['id'])

    # ### end Alembic commands ###
