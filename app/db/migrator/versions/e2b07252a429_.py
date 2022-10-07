"""empty message

Revision ID: e2b07252a429
Revises: d273105942bb
Create Date: 2022-10-08 01:39:15.193658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2b07252a429'
down_revision = 'd273105942bb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('descriotion', sa.VARCHAR(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'descriotion')
    # ### end Alembic commands ###