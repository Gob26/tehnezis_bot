"""add_added_at_column_to_crawling_target

Revision ID: 2f79174ecc36
Revises: 6179cf95f254
Create Date: 2025-04-15 17:34:16.558371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f79174ecc36'
down_revision: Union[str, None] = '6179cf95f254'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
