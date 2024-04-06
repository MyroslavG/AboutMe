"""Pdf_url added

Revision ID: 02a3f8ae232d
Revises: 94fe1c039013
Create Date: 2024-04-05 23:57:03.386348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02a3f8ae232d'
down_revision = '94fe1c039013'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pdf_url', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('pdf_url')

    # ### end Alembic commands ###
