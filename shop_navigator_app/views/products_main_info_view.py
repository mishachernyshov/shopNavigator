"""
Contains tools for providing main information about products.
"""

from flask_restful import Resource
from shop_navigator_app.service.product_service \
    import ProductService

from shop_navigator_app import db


class ProductsMainInfoView(Resource):
    """
    Contains methods for getting HTTP-requests and sending HTTP-responses
    to provide APIs to provide main information about products.
    """

    def get(self):
        """
        :return: response with main information about products
        """
        products_main_info = ProductService.get_main_info(db.session)
        response_data = self.structure_product_dict(products_main_info)
        return response_data, 200

    @staticmethod
    def structure_product_dict(products_main_info):
        """
        :param products_main_info: the selected products main information
        from the database
        :return: the selected products main information in JSON format
        """
        result_dict = dict()
        for product_main_info in products_main_info:
            result_dict[product_main_info[0]] = product_main_info[1]
        return result_dict
