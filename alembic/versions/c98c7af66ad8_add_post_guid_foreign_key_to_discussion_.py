"""Add post_guid foreign key to discussion table

Revision ID: c98c7af66ad8
Revises: b19431af8cb2
Create Date: 2020-10-10 10:00:20.882425

"""
from alembic import op
import sqlalchemy as sa
import fastapi_utils


# revision identifiers, used by Alembic.
revision = 'c98c7af66ad8'
down_revision = 'b19431af8cb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('discussions', sa.Column('post_guid', fastapi_utils.guid_type.GUID(), nullable=True))
    op.create_foreign_key(None, 'discussions', 'discussions', ['post_guid'], ['guid'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'discussions', type_='foreignkey')
    op.drop_column('discussions', 'post_guid')
    # ### end Alembic commands ###