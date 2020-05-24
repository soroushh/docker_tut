"""create_people_table

Revision ID: 0786c12a358e
Revises: a0af8050ebc7
Create Date: 2020-05-24 11:56:49.704186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0786c12a358e'
down_revision = 'a0af8050ebc7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'people',
        sa.Column('person_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('family', sa.String)
    )


def downgrade():
    op.drop_table('people')
