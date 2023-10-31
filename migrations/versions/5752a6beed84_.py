"""empty message

Revision ID: 5752a6beed84
Revises: 
Create Date: 2023-03-19 17:15:18.721141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5752a6beed84'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_name', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=125), nullable=False),
    sa.Column('user_email', sa.String(length=80), nullable=False),
    sa.Column('user_phone', sa.Integer(), nullable=False),
    sa.Column('rdatetime', sa.DateTime(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
