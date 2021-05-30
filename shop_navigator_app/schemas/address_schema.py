"""
Provides powerful tools for validating address data and
quick loading and dumping address models.
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from shop_navigator_app.models.address import Address


class AddressSchema(SQLAlchemyAutoSchema):
    """
    Specifies the address schema structure.
    """

    class Meta:
        """
        Describes the address model metadata.
        """
        model = Address
        load_instance = True
        include_fk = True
