"""image_file length updated

Revision ID: 462383195014
Revises: 4af9639495b8
Create Date: 2023-08-04 10:22:11.838972

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '462383195014'
down_revision = '4af9639495b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('image_file',
               existing_type=mysql.VARCHAR(length=20),
               type_=sa.String(length=200),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('image_file',
               existing_type=sa.String(length=200),
               type_=mysql.VARCHAR(length=20),
               existing_nullable=True)

    # ### end Alembic commands ###
