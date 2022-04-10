"""Make Municipality.has_board NOT nullable

Revision ID: fc790958f463
Revises: 1ac54fa65e2c
Create Date: 2022-04-10 15:58:54.450169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc790958f463'
down_revision = '1ac54fa65e2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('municipality', 'has_board',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('municipality', 'has_board',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###