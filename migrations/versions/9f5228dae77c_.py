"""empty message

Revision ID: 9f5228dae77c
Revises: 
Create Date: 2020-09-27 18:23:39.205492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f5228dae77c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('DatasetManager',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('datasetName', sa.String(length=255), nullable=False),
    sa.Column('datasetSqlName', sa.String(length=255), nullable=False),
    sa.Column('createDateTime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_DatasetManager')),
    sa.UniqueConstraint('datasetName', name=op.f('uq_DatasetManager_datasetName')),
    sa.UniqueConstraint('datasetSqlName', name=op.f('uq_DatasetManager_datasetSqlName'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('DatasetManager')
    # ### end Alembic commands ###
