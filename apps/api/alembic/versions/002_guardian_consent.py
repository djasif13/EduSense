"""Guardian consent table
Revision ID: 002
Revises: 001
"""
from alembic import op
import sqlalchemy as sa

revision = '002'
down_revision = '001'

def upgrade():
    op.create_table('guardian_consents',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('learner_id', sa.Text(), nullable=False),
        sa.Column('guardian_email_hash', sa.Text(), nullable=False),
        sa.Column('consent_given', sa.Boolean(), nullable=False),
        sa.Column('consent_timestamp', sa.TIMESTAMP(timezone=True)),
        sa.Column('modalities_consented', sa.ARRAY(sa.Text())),
        sa.Column('revoked_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('audit_trail', sa.JSON()),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('guardian_consents')
