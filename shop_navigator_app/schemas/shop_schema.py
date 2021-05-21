from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from shop_navigator_app.models.shop import Shop


class ShopSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Shop
        load_instance = True
        include_fk = True
