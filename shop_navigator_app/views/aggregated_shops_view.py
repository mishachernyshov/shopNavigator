from flask_restful import Resource
from shop_navigator_app.models.shop import Shop, shops_products
from shop_navigator_app.models.address import Address
from shop_navigator_app.schemas.shop_schema import ShopSchema
from shop_navigator_app.schemas.address_schema import AddressSchema

from .. import db
from sqlalchemy import func


class AggregatedShopsView(Resource):
    def get(self):
        shop_aggregate_list = db.session.query(
            Shop,
            Address,
            func.count(shops_products.columns.product_id)
            .label('product_count'),
            func.avg(shops_products.columns.price)
            .label('average_price')
        ).join(Address).outerjoin(shops_products).group_by(Shop, Address).all()
        serialized_shops = self.serialize_shop_aggregate_list(
            shop_aggregate_list
        )
        return serialized_shops, 200

    def serialize_shop_aggregate_list(self, shops):
        serialized_shop_list = list()
        shop_schema = ShopSchema(exclude=['address_id'])
        address_schema = AddressSchema()
        for shop in shops:
            serialized_shop = shop_schema.dump(shop.Shop)
            serialized_shop['product_count'] = shop.product_count
            serialized_shop['average_price'] = float(shop.average_price) \
                if shop.average_price else None
            serialized_shop['address'] = address_schema.dump(shop.Address)
            serialized_shop_list.append(serialized_shop)
            print(serialized_shop)
        return serialized_shop_list
