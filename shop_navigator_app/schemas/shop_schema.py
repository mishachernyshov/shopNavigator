"""
Provides powerful tools for validating shop data and
quick loading and dumping shop models.
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from shop_navigator_app.models.shop import Shop


class ShopSchema(SQLAlchemyAutoSchema):
    """
    Specifies the shop schema structure.
    """

    class Meta:
        """
        Describes the shop model metadata.
        """
        model = Shop
        load_instance = True
        include_fk = True
