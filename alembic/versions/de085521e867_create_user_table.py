"""create user table

Revision ID: de085521e867
Revises: 0786c12a358e
Create Date: 2020-05-24 18:16:45.178599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de085521e867'
down_revision = '0786c12a358e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('user_id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String),
        sa.Column('email', sa.String),
        sa.Column('password', sa.String),
        sa.Column('image_file', sa.String)
    )


def downgrade():
    op.drop_table('user')
