"""Create conversation tables

Revision ID: 001_conversation_tables
Revises: 
Create Date: 2026-01-14 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import uuid
from datetime import datetime

# revision identifiers
revision = '001_conversation_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create conversation_thread table
    op.create_table(
        'conversation_thread',
        sa.Column('id', sa.Uuid, primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', sa.Uuid, nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow, nullable=False),
        sa.Column('updated_at', sa.DateTime, default=datetime.utcnow, nullable=False),
        sa.Column('active', sa.Boolean, default=True, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    )

    # Create conversation_message table
    op.create_table(
        'conversation_message',
        sa.Column('id', sa.Uuid, primary_key=True, default=uuid.uuid4),
        sa.Column('thread_id', sa.Uuid, nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow, nullable=False),
        sa.ForeignKeyConstraint(['thread_id'], ['conversation_thread.id'], ondelete='CASCADE'),
        sa.CheckConstraint("role IN ('user', 'assistant')", name='role_check'),
    )

    # Create indexes
    op.create_index('idx_conversation_thread_user_id', 'conversation_thread', ['user_id'])
    op.create_index('idx_conversation_message_thread_id', 'conversation_message', ['thread_id'])
    op.create_index('idx_conversation_message_created_at', 'conversation_message', ['created_at'])


def downgrade():
    # Drop indexes
    op.drop_index('idx_conversation_message_created_at', table_name='conversation_message')
    op.drop_index('idx_conversation_message_thread_id', table_name='conversation_message')
    op.drop_index('idx_conversation_thread_user_id', table_name='conversation_thread')

    # Drop tables
    op.drop_table('conversation_message')
    op.drop_table('conversation_thread')