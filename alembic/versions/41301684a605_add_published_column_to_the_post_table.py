"""add published column to the post table 

Revision ID: 41301684a605
Revises: 122d624f3c6e
Create Date: 2026-03-25 17:08:05.976003

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41301684a605'
down_revision: Union[str, Sequence[str], None] = '122d624f3c6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    pass
