"""Create tables 2

Revision ID: 8263386f5bc9
Revises: 4d4d55f8494f
Create Date: 2024-04-07 11:42:56.804469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8263386f5bc9'
down_revision: Union[str, None] = '4d4d55f8494f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
