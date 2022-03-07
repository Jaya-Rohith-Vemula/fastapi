"""add user table

Revision ID: 817645d1178b
Revises: 8529a76e072a
Create Date: 2022-03-07 19:31:54.914557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '817645d1178b'
down_revision = '8529a76e072a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
