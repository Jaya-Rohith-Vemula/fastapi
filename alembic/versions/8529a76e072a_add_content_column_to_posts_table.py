"""add content column to posts table

Revision ID: 8529a76e072a
Revises: 5b2bded74849
Create Date: 2022-03-07 19:29:08.184458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8529a76e072a'
down_revision = '5b2bded74849'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass