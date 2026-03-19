"""create database

Revision ID: 7058a2764e8e
Revises: f6e647d9946d
Create Date: 2026-03-15 19:55:10.517147

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7058a2764e8e'
down_revision: Union[str, Sequence[str], None] = 'f6e647d9946d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
