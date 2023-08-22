"""initial customer migration

Revision ID: e6303a2ee872
Revises: 
Create Date: 2023-08-22 14:17:21.271614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6303a2ee872'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('billing_profiles',
    sa.Column('billing_profile_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('card_number', sa.Integer(), nullable=False),
    sa.Column('card_name', sa.String(length=20), nullable=False),
    sa.Column('expiry_date', sa.String(length=10), nullable=False),
    sa.Column('cvv', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('billing_profile_id')
    )
    op.create_index(op.f('ix_billing_profiles_billing_profile_id'), 'billing_profiles', ['billing_profile_id'], unique=False)
    op.create_table('customers',
    sa.Column('customer_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('primary_email', sa.String(length=45), nullable=False),
    sa.Column('secondary_email', sa.String(length=45), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=False),
    sa.Column('last_name', sa.String(length=20), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('birthdate', sa.String(length=10), nullable=False),
    sa.Column('registration_date', sa.Integer(), nullable=False),
    sa.Column('role', sa.Enum('SUPER_ADMIN', 'ADMIN', 'SUPER_USER', 'USER', name='roles'), nullable=False),
    sa.PrimaryKeyConstraint('customer_id'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_index(op.f('ix_customers_customer_id'), 'customers', ['customer_id'], unique=False)
    op.create_index(op.f('ix_customers_primary_email'), 'customers', ['primary_email'], unique=True)
    op.create_index(op.f('ix_customers_username'), 'customers', ['username'], unique=True)
    op.create_table('test',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_id'), 'test', ['id'], unique=False)
    op.create_table('lookup_customer_billings',
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('billing_profile_id', sa.Integer(), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['billing_profile_id'], ['billing_profiles.billing_profile_id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], ),
    sa.PrimaryKeyConstraint('customer_id', 'billing_profile_id')
    )
    op.create_index(op.f('ix_lookup_customer_billings_billing_profile_id'), 'lookup_customer_billings', ['billing_profile_id'], unique=False)
    op.create_index(op.f('ix_lookup_customer_billings_customer_id'), 'lookup_customer_billings', ['customer_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_lookup_customer_billings_customer_id'), table_name='lookup_customer_billings')
    op.drop_index(op.f('ix_lookup_customer_billings_billing_profile_id'), table_name='lookup_customer_billings')
    op.drop_table('lookup_customer_billings')
    op.drop_index(op.f('ix_test_id'), table_name='test')
    op.drop_table('test')
    op.drop_index(op.f('ix_customers_username'), table_name='customers')
    op.drop_index(op.f('ix_customers_primary_email'), table_name='customers')
    op.drop_index(op.f('ix_customers_customer_id'), table_name='customers')
    op.drop_table('customers')
    op.drop_index(op.f('ix_billing_profiles_billing_profile_id'), table_name='billing_profiles')
    op.drop_table('billing_profiles')
    # ### end Alembic commands ###
