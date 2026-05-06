"""Initial schema

Revision ID: 001
Create Date: 2026-05-06
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None

def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
    
    op.create_table('learner_events',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('session_id', sa.Text(), nullable=False),
        sa.Column('learner_id', sa.Text(), nullable=False),
        sa.Column('content_id', sa.Text()),
        sa.Column('section_id', sa.Text()),
        sa.Column('timestamp', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('learner_state', sa.Text()),
        sa.Column('state_confidence', sa.Float()),
        sa.Column('signals', sa.JSON()),
        sa.Column('privacy_class', sa.Text()),
        sa.Column('consent_scope', sa.ARRAY(sa.Text())),
        sa.PrimaryKeyConstraint('id', 'timestamp')
    )
    op.execute("SELECT create_hypertable('learner_events', 'timestamp');")

    op.create_table('consent_records',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('learner_id', sa.Text(), nullable=False),
        sa.Column('modality', sa.Text(), nullable=False),
        sa.Column('granted', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('consent_records')
    op.drop_table('learner_events')
