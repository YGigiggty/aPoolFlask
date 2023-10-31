"""empty message

Revision ID: 8f00b92bffad
Revises: 3596b3f150eb
Create Date: 2023-04-01 10:03:07.423109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f00b92bffad'
down_revision = '3596b3f150eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar_bytea', sa.LargeBinary(length=3600), nullable=False))
        batch_op.drop_column('avatar_hash')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar_hash', sa.VARCHAR(length=200), autoincrement=False, nullable=True))
        batch_op.drop_column('avatar_bytea')

    # ### end Alembic commands ###