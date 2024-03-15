"""media column added to the post model

Revision ID: 4cd22f6e8a56
Revises: fd6e387ce9fa
Create Date: 2023-08-14 22:20:30.973178

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4cd22f6e8a56'
down_revision = 'fd6e387ce9fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('video_file')
        batch_op.drop_column('picture_file')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture_file', mysql.VARCHAR(length=200), nullable=True))
        batch_op.add_column(sa.Column('video_file', mysql.VARCHAR(length=200), nullable=True))

    # ### end Alembic commands ###
