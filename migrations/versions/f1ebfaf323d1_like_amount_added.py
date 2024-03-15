"""like_amount added

Revision ID: f1ebfaf323d1
Revises: 24fd3775a092
Create Date: 2023-08-03 10:23:30.755090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1ebfaf323d1'
down_revision = '24fd3775a092'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('like_amount', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('like_amount')

    # ### end Alembic commands ###