"""Add role_id to user table

Revision ID: 743e105c885b
Revises: 
Create Date: 2024-07-01 12:25:12.879147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '743e105c885b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_auth_id', table_name='auth')
    op.drop_index('ix_auth_username', table_name='auth')
    op.drop_table('auth')
    op.drop_index('ix_role_name', table_name='role')
    op.create_unique_constraint(None, 'role', ['name'])
    op.add_column('user', sa.Column('role_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'role', ['role_id'], ['id'])
    op.drop_column('user', 'hashed_password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'role_id')
    op.drop_constraint(None, 'role', type_='unique')
    op.create_index('ix_role_name', 'role', ['name'], unique=True)
    op.create_table('auth',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='auth_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='auth_pkey')
    )
    op.create_index('ix_auth_username', 'auth', ['username'], unique=True)
    op.create_index('ix_auth_id', 'auth', ['id'], unique=False)
    # ### end Alembic commands ###
