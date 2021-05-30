"""
Provides powerful tools for validating shop product data and
quick loading and dumping shop product table entities.
"""

from marshmallow import Schema, fields


class ShopProductsSchema(Schema):
    """
    Specifies the shop product schema structure.
    """
    shop_id = fields.Integer()
    product_id = fields.Integer()
    price = fields.Float()
    count = fields.Integer()
    name = fields.String()
