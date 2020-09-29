"""Create dicussion table

Revision ID: 58dd29a7931e
Revises: 3f47755f2312
Create Date: 2020-09-28 21:18:54.587134

"""
from alembic import op
import sqlalchemy as sa
import fastapi_utils


# revision identifiers, used by Alembic.
revision = '58dd29a7931e'
down_revision = '3f47755f2312'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('discussions',
    sa.Column('guid', fastapi_utils.guid_type.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('author_guid', fastapi_utils.guid_type.GUID(), nullable=False),
    sa.Column('enrollment_guid', fastapi_utils.guid_type.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['author_guid'], ['users.guid'], ),
    sa.ForeignKeyConstraint(['enrollment_guid'], ['enrollments.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_discussions_guid'), 'discussions', ['guid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_discussions_guid'), table_name='discussions')
    op.drop_table('discussions')
    # ### end Alembic commands ###