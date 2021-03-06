"""Initial migration

Revision ID: d1c2828d49cd
Revises: 
Create Date: 2022-04-10 15:13:27.660338

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd1c2828d49cd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'mapper', ['ruian'])
    op.drop_column('mapper', 'location_longitude')
    op.drop_column('mapper', 'location_latitude')
    op.add_column('municipality', sa.Column('has_board', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'municipality', ['ruian'])
    op.add_column('notice_document', sa.Column('shortened_extracted_text', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notice_document', 'shortened_extracted_text')
    op.drop_constraint(None, 'municipality', type_='unique')
    op.drop_column('municipality', 'has_board')
    op.add_column('mapper', sa.Column('location_latitude', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('mapper', sa.Column('location_longitude', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'mapper', type_='unique')
    # ### end Alembic commands ###
