"""empty message

Revision ID: 8976b8165527
Revises: 19c2d5ef1bb8
Create Date: 2020-09-28 08:49:04.143293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8976b8165527'
down_revision = '19c2d5ef1bb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ResearchInfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('weblink', sa.String(length=500), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('tags', sa.String(length=500), nullable=True),
    sa.Column('createDateTime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_ResearchInfo'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ResearchInfo')
    # ### end Alembic commands ###
