"""create posts table

Revision ID: 10974f1972a5
Revises: 311b596854b1
Create Date: 2026-03-25 16:59:28.868772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10974f1972a5'
down_revision: Union[str, Sequence[str], None] = '311b596854b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
