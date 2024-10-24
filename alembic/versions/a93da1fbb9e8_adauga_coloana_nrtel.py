"""adauga coloana nrtel

Revision ID: a93da1fbb9e8
Revises: e8120be5637e
Create Date: 2024-10-10 16:51:41.247921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy import Column, INTEGER, ForeignKey  #adaugat pt nevoile de aici


# revision identifiers, used by Alembic.
revision: str = 'a93da1fbb9e8'
down_revision: Union[str, None] = 'e8120be5637e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("users", Column("nrtel", INTEGER))
    pass

def downgrade():
    op.drop_column('users','nrtel')
    pass