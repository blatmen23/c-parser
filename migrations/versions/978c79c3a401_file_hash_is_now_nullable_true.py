"""file_hash is now nullable true

Revision ID: 978c79c3a401
Revises: 72a6024af995
Create Date: 2025-02-24 22:14:10.664110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '978c79c3a401'
down_revision: Union[str, None] = '72a6024af995'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('media_contents', 'file_hash',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('media_contents', 'file_hash',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###
