"""empty message

Revision ID: ae0471ffa52b
Revises: 5a94915c9ac2
Create Date: 2023-05-31 22:00:24.498089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae0471ffa52b'
down_revision = '5a94915c9ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_index('article_fts_gin_index')
        batch_op.create_index('ix_post___ts_vector__', ['fts'], unique=False, postgresql_using='gin')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_index('ix_post___ts_vector__', postgresql_using='gin')
        batch_op.create_index('article_fts_gin_index', ['fts'], unique=False)

    # ### end Alembic commands ###
