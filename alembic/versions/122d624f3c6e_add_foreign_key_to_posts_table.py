"""add foreign key to posts table

Revision ID: 122d624f3c6e
Revises: 10974f1972a5
Create Date: 2026-03-25 17:01:55.768899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '122d624f3c6e'
down_revision: Union[str, Sequence[str], None] = '10974f1972a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
