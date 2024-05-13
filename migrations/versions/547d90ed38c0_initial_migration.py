"""Initial migration.

Revision ID: 547d90ed38c0
Revises: 
Create Date: 2024-05-10 18:39:48.142370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '547d90ed38c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('municipality',
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('has_extended_competence', sa.Boolean(), nullable=False),
    sa.Column('ico', sa.Integer(), nullable=True),
    sa.Column('ruian', sa.Integer(), nullable=False),
    sa.Column('parent_ruian', sa.Integer(), nullable=True),
    sa.Column('has_board', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['parent_ruian'], ['municipality.ruian'], ),
    sa.PrimaryKeyConstraint('ruian'),
    sa.UniqueConstraint('ico'),
    sa.UniqueConstraint('ruian')
    )
    op.create_table('official_notice_board',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('office_name', sa.String(length=100), nullable=True),
    sa.Column('office_name_missing', sa.Boolean(), nullable=False),
    sa.Column('ico', sa.Integer(), nullable=True),
    sa.Column('ico_missing', sa.Boolean(), nullable=False),
    sa.Column('municipality_ruian', sa.Integer(), nullable=True),
    sa.Column('download_url', sa.String(length=255), nullable=True),
    sa.Column('download_url_missing', sa.Boolean(), nullable=False),
    sa.Column('download_url_unreachable', sa.Boolean(), nullable=False),
    sa.Column('attempted_download', sa.Boolean(), nullable=False),
    sa.Column('notices_missing', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['municipality_ruian'], ['municipality.ruian'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('iri', sa.String(length=1024), nullable=True),
    sa.Column('iri_missing', sa.Boolean(), nullable=False),
    sa.Column('url', sa.String(length=1024), nullable=True),
    sa.Column('url_missing', sa.Boolean(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('name_missing', sa.Boolean(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('description_missing', sa.Boolean(), nullable=False),
    sa.Column('reference_number', sa.String(length=255), nullable=True),
    sa.Column('reference_number_missing', sa.Boolean(), nullable=False),
    sa.Column('revision', sa.String(length=100), nullable=True),
    sa.Column('post_date', sa.DateTime(), nullable=True),
    sa.Column('post_date_wrong_format', sa.Boolean(), nullable=False),
    sa.Column('relevant_until_date', sa.DateTime(), nullable=True),
    sa.Column('relevant_until_date_wrong_format', sa.Boolean(), nullable=False),
    sa.Column('documents_missing', sa.Boolean(), nullable=False),
    sa.Column('documents_wrong_format', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['board_id'], ['official_notice_board.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notice_document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('notice_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=1024), nullable=True),
    sa.Column('name_missing', sa.Boolean(), nullable=False),
    sa.Column('download_url', sa.String(length=1024), nullable=True),
    sa.Column('download_url_missing', sa.Boolean(), nullable=False),
    sa.Column('attempted_download', sa.Boolean(), nullable=False),
    sa.Column('download_url_unreachable', sa.Boolean(), nullable=False),
    sa.Column('downloaded_file_path', sa.String(length=255), nullable=True),
    sa.Column('file_extension', sa.String(length=10), nullable=True),
    sa.Column('file_missing', sa.Boolean(), nullable=False),
    sa.Column('attempted_extraction', sa.Boolean(), nullable=False),
    sa.Column('extraction_fail', sa.Boolean(), nullable=False),
    sa.Column('extracted_text', sa.Text(), nullable=True),
    sa.Column('shortened_extracted_text', sa.String(length=100), nullable=True),
    sa.Column('file_contains_no_text', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['notice_id'], ['notice.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notice_document')
    op.drop_table('notice')
    op.drop_table('official_notice_board')
    op.drop_table('municipality')
    # ### end Alembic commands ###
