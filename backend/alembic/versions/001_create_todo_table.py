"""Create todo table

Revision ID: 001
Revises:
Create Date: 2025-12-28

Note: User, Session, and Account tables are created by Better Auth.
This migration only creates the Todo table managed by FastAPI.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Note: user table is created by Better Auth
    # We create todo table without FK first, then add FK if user table exists
    op.create_table(
        'todo',
        sa.Column('id', sa.UUID(), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=False),
        sa.Column('is_complete', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_todo_user_id', 'todo', ['user_id'])

    # Try to add FK constraint if user table exists (created by Better Auth)
    try:
        op.create_foreign_key(
            'fk_todo_user_id',
            'todo', 'user',
            ['user_id'], ['id'],
            ondelete='CASCADE'
        )
    except Exception:
        # FK will be added later when user table exists
        pass


def downgrade() -> None:
    op.drop_index('idx_todo_user_id', table_name='todo')
    op.drop_table('todo')
