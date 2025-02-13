"""History table added, VPS table updated with relationship 2

Revision ID: 53a517ad4ead
Revises: a98abfe29bc5
Create Date: 2025-02-13 13:01:54.332767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53a517ad4ead'
down_revision: Union[str, None] = 'a98abfe29bc5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vps_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('data', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['vps_id'], ['vps.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('history')
    # ### end Alembic commands ###
