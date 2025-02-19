"""empty message

Revision ID: a2405bfcd62d
Revises: 1ee4b16715cb
Create Date: 2023-12-04 12:43:05.591848

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2405bfcd62d'
down_revision: Union[str, None] = '1ee4b16715cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stocks', sa.Column('asset_ype', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stocks', 'asset_ype')
    # ### end Alembic commands ###
