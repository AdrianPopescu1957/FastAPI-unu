"""adauga coloana nrtel

Revision ID: 0040ec531d9a
Revises: a93da1fbb9e8
Create Date: 2024-10-10 16:54:25.372694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0040ec531d9a'
down_revision: Union[str, None] = 'a93da1fbb9e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
