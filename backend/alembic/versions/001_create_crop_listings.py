"""Create crop_listings table

Revision ID: 001_crop_listings
Revises: 
Create Date: 2026-07-29

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_crop_listings'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'crop_listings',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('farmer_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('plot_id', sa.String(length=36), nullable=True),
        sa.Column('crop', sa.String(length=100), nullable=False, index=True),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('expected_price', sa.Float(), nullable=False),
        sa.Column('harvest_date', sa.Date(), nullable=True),
        sa.Column('quality_grade', sa.String(length=50), server_default='Grade A'),
        sa.Column('location', sa.String(length=200), nullable=True, index=True),
        sa.Column('available_until', sa.Date(), nullable=True),
        sa.Column('photo_url', sa.String(length=500), nullable=True),
        sa.Column('status', sa.String(length=20), server_default='ACTIVE'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade():
    op.drop_table('crop_listings')
