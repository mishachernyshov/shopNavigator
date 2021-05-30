"""
The module that provides functionality to work with aggregated
information about shops.
"""

from flask_restful import Resource
from shop_navigator_app.schemas.shop_schema import ShopSchema
from shop_navigator_app.schemas.address_schema import AddressSchema

from shop_navigator_app import db
from shop_navigator_app.service.aggregated_shops_service \
    import AggregatedShopsService


class AggregatedShopsView(Resource):
    """
    Gives tools for working with aggregated statistics info
    about shops to clients.
    """

    def get(self):
        """
        Provides a list of the shops with basic info from database
        together with aggregated values such as product count
        in the shop and the average price in it.
        :return: response which consists of shops data in JSON format
                 and status code.
        """
        shop_aggregate_list = \
            AggregatedShopsService.get_aggregated_shops_list(
                db.session
            )
        serialized_shops = self.serialize_shop_aggregate_list(
            shop_aggregate_list
        )
        return serialized_shops, 200

    @staticmethod
    def serialize_shop_aggregate_list(shops):
        """
        :param shops: the selected aggregated data from the database
        about shops
        :return: the selected aggregated data in JSON format
        """
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
        return serialized_shop_list
