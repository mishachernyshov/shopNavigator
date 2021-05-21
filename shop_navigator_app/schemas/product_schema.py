from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from shop_navigator_app.models.product import Product


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
