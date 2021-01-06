"""empty message

Revision ID: b9ee518b723b
Revises: 95ce63101c6c
Create Date: 2021-01-06 23:24:56.838761

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b9ee518b723b'
down_revision = '95ce63101c6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('name', table_name='organizations')
    op.drop_table('organizations')
    op.drop_constraint('products_ibfk_1', 'products', type_='foreignkey')
    op.drop_column('products', 'organization_id')
    op.drop_constraint('user_ibfk_1', 'user', type_='foreignkey')
    op.drop_column('user', 'organization_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('organization_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('user_ibfk_1', 'user', 'organizations', ['organization_id'], ['id'])
    op.add_column('products', sa.Column('organization_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('products_ibfk_1', 'products', 'organizations', ['organization_id'], ['id'])
    op.create_table('organizations',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=120), nullable=False),
    sa.Column('address1', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('address2', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('city', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('state', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('zipCode', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('phone_number', mysql.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('name', 'organizations', ['name'], unique=True)
    # ### end Alembic commands ###