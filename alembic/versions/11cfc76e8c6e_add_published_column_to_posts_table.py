"""add published column to posts table

Revision ID: 11cfc76e8c6e
Revises: e1fd27dc12b3
Create Date: 2025-09-06 16:26:08.083173

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11cfc76e8c6e'
down_revision: Union[str, Sequence[str], None] = 'e1fd27dc12b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default=sa.true(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    pass
