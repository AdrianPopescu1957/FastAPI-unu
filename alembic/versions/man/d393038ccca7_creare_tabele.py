"""creare tabele

Revision ID: d393038ccca7
Revises: 
Create Date: 2024-10-10 16:26:29.682060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from datetime import datetime #modulul operatiilor cu timpul; folosit pt a inregistra momentul operatiunii


# revision identifiers, used by Alembic.
revision: str = 'd393038ccca7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.create_table ('posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('titlu', sa.String(), nullable=False),
        sa.Column('continut', sa.String(), nullable=False),
        sa.Column('apreciere', sa.Integer(), nullable=True),
        sa.Column('ciorna', sa.Boolean, default=True))
    op.create_table ('users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('parola', sa.String(), nullable=False),
        sa.Column('moment', sa.String(), nullable=True, server_default=str(datetime.now())))
    op.create_table("voturi")
    pass


def downgrade():
    op.drop_table('voturi')
    op.drop_table('posts')
    op.drop_table('users')
    pass