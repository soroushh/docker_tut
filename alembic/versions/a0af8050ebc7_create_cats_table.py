"""create_cats_table

Revision ID: a0af8050ebc7
Revises: 
Create Date: 2020-05-24 11:17:01.152629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0af8050ebc7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cats',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('price', sa.Integer, default=1368),
        sa.Column('breed', sa.String)
    )


def downgrade():
    op.drop_table('cats')

