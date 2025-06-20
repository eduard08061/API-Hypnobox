"""fix nullable fields  model products

Revision ID: 4f6274db1132
Revises: dd7248abb3c0
Create Date: 2024-05-28 00:15:54.712416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '4f6274db1132'
down_revision: Union[str, None] = 'dd7248abb3c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('hy_product_addresses', 'Cep',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('hy_product_addresses', 'Logradouro',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('hy_product_addresses', 'Numero',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('hy_product_addresses', 'Complemento',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('hy_product_addresses', 'Estado',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('hy_product_addresses', 'Cidade',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('hy_product_addresses', 'Bairro',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('hy_product_units', 'TipoUnidade',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('hy_product_units', 'Finalidade',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('hy_product_units', 'Transacao',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('hy_product_units', 'TotalComodos',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('hy_product_units', 'TotalDormitorio',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('hy_product_units', 'TotalAreaUtil',
               existing_type=mysql.FLOAT(),
               nullable=True)
    op.alter_column('hy_product_units', 'TotalAreaTotal',
               existing_type=mysql.FLOAT(),
               nullable=True)
    op.alter_column('hy_product_units', 'TotalSuite',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('hy_product_units', 'TotalBanheiro',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('hy_product_units', 'TotalVaga',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('hy_product_units', 'TotalPeDireito',
               existing_type=mysql.FLOAT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('hy_product_units', 'TotalPeDireito',
               existing_type=mysql.FLOAT(),
               nullable=False)
    op.alter_column('hy_product_units', 'TotalVaga',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('hy_product_units', 'TotalBanheiro',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('hy_product_units', 'TotalSuite',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('hy_product_units', 'TotalAreaTotal',
               existing_type=mysql.FLOAT(),
               nullable=False)
    op.alter_column('hy_product_units', 'TotalAreaUtil',
               existing_type=mysql.FLOAT(),
               nullable=False)
    op.alter_column('hy_product_units', 'TotalDormitorio',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('hy_product_units', 'TotalComodos',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('hy_product_units', 'Transacao',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('hy_product_units', 'Finalidade',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('hy_product_units', 'TipoUnidade',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('hy_product_addresses', 'Bairro',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('hy_product_addresses', 'Cidade',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('hy_product_addresses', 'Estado',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('hy_product_addresses', 'Complemento',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('hy_product_addresses', 'Numero',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('hy_product_addresses', 'Logradouro',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('hy_product_addresses', 'Cep',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
