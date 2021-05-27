from marshmallow import Schema, fields


class ShopProductsSchema(Schema):
    shop_id = fields.Integer()
    product_id = fields.Integer()
    price = fields.Float()
    count = fields.Integer()
    name = fields.String()
