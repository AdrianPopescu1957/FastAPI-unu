"""creaza tabelele initiale

Revision ID: 4c0ba3b6842a
Revises: 
Create Date: 2024-10-31 12:51:01.248818

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from datetime import datetime #modulul operatiilor cu timpul; folosit pt a inregistra momentul operatiunii


# revision identifiers, used by Alembic.
revision: str = '4c0ba3b6842a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.create_table ('users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('parola', sa.String(), nullable=False),
        sa.Column('moment', sa.String(), nullable=True, server_default=str(datetime.now())))

    op.create_table ('posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('titlu', sa.String(), nullable=False),
        sa.Column('ciorna', sa.Boolean(), nullable=True),
        sa.Column('continut', sa.String(), default='Continutul articolului', nullable=False),
        sa.Column('apreciere', sa.Integer(), nullable=True),
        sa.Column('idproprietar', sa.Integer(), 
                   sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        #sa.Column('telmobil', sa.Integer(), nullable=True)
        #sa.Column('proprietar', Relationship("User")) sintaxa cf modele6.py, probabil gresit
                        )
    
    op.create_table("voturi",
        sa.Column("iduser", sa.INTEGER, sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("idart", sa.INTEGER, sa.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True))

    pass


def downgrade():
    op.drop_table('voturi')
    op.drop_table('posts')
    op.drop_table('users')
    pass
