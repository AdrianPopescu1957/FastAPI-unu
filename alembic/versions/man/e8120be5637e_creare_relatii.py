"""creare relatii

Revision ID: e8120be5637e
Revises: d393038ccca7
Create Date: 2024-10-10 16:29:58.479917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy import Column, INTEGER, ForeignKey  #adaugat pt nevoile de aici

# revision identifiers, used by Alembic.
revision: str = 'e8120be5637e'
down_revision: Union[str, None] = 'd393038ccca7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("posts", Column("idproprietar", INTEGER, ForeignKey("users.id")))
    op.add_column("voturi",Column("iduser", INTEGER, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True))
    op.add_column("voturi",Column("idart", INTEGER, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True))
    #op.add_column("voturi",Column("iduser", INTEGER, ForeignKey("users.id", ondelete="CASCADE")))
    #op.add_column("voturi",Column("idart", INTEGER, ForeignKey("posts.id", ondelete="CASCADE")))
    #sa.PrimaryKeyConstraint("iduser","idart")
    pass

def downgrade():
    op.drop_column('voturi','idart')
    op.drop_column('voturi','iduser')
    op.drop_column('posts','idproprietar')
    pass