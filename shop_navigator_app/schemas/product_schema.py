"""
Provides powerful tools for validating product data and
quick loading and dumping product models.
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from shop_navigator_app.models.product import Product


class ProductSchema(SQLAlchemyAutoSchema):
    """
    Specifies the address schema structure.
    """

    class Meta:
        """
        Describes the product model metadata.
        """
        model = Product
        load_instance = True
