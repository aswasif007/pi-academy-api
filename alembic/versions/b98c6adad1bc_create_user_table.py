"""Create user table

Revision ID: b98c6adad1bc
Revises: 5cd97979b401
Create Date: 2020-09-26 21:32:30.085602

"""
from alembic import op
import sqlalchemy as sa
import fastapi_utils

# revision identifiers, used by Alembic.
revision = 'b98c6adad1bc'
down_revision = '5cd97979b401'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('guid', fastapi_utils.guid_type.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.VARCHAR(length=128), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('category', sa.VARCHAR(length=64), nullable=False),
    sa.PrimaryKeyConstraint('guid'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_guid'), 'users', ['guid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_guid'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
