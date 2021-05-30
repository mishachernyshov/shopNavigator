"""
Contains tools for executing CRUD operations with shop products
and selecting information about shop product entities by users via APIs.
"""

from flask_restful import Resource
from marshmallow import ValidationError
from flask import request

from shop_navigator_app.models.shop import shops_products
from shop_navigator_app.service.shop_product_service \
    import ShopProductService
from shop_navigator_app.service.shop_service import ShopService
from shop_navigator_app.schemas.shop_products_schema \
    import ShopProductsSchema
from shop_navigator_app import db


class ShopProductsView(Resource):
    """
    Contains methods for getting HTTP-requests and sending HTTP-responses
    to provide APIs to work with shop product table.
    """

    def get(self, instance_id=None):
        """
        :param instance_id: resource identificator to get a specific
                            shop product instance
        :return: if correct instance_id is specified, the function returns the
                 response with product list of shop that has specified id; if the
                 identificator is wrong or it is missed, an empty JSON object
                 will be returned
        """
        if not instance_id:
            return {}, 404
        min_price, max_price, exact_price = self.get_params(request.args)
        conditions = self.get_conditions(exact_price, min_price, max_price)
        shop_name = ShopService.get_shop_name(db.session, instance_id)
        shop_products = ShopProductService.get_shop_products(
            db.session, instance_id, conditions
        )
        response = self.make_response(shop_name, shop_products)
        return response, 200

    @staticmethod
    def get_params(request_arguments):
        """
        :param request_arguments: the request parameters list
        :return: passed price parameters tuple
        """
        min_price = request_arguments.get('min_price')
        max_price = request_arguments.get('max_price')
        exact_price = request_arguments.get('exact_price')

        return min_price, max_price, exact_price

    @staticmethod
    def get_conditions(exact_price, min_price, max_price):
        """
        :param exact_price: exact price value
        :param min_price: the minimum value of the price range
        :param max_price: the maximum value of the price range
        :return: list of conditions for filtering products by price
        """
        conditions = []

        if exact_price:
            conditions.append(
                shops_products.columns.price == exact_price
            )
        else:
            if min_price:
                conditions.append(
                    shops_products.columns.price >= min_price
                )
            if max_price:
                conditions.append(
                    shops_products.columns.price <= max_price
                )
        return conditions

    @staticmethod
    def make_response(shop_name, shop_products):
        """
        :param shop_name: the current shop name
        :param shop_products: all found products that the current shop contains
        :return: information about all shop products in a user-friendly form
                 in JSON format
        """
        return {
            'name': shop_name,
            'products': ShopProductsSchema().dump(shop_products, many=True)
        }

    def post(self):
        """
        Creates a shop product table row with the provided data.
        :return: if the correct data passed, a response with
                 the new instance info will be returned;
                 otherwise, a response body will contain an
                 error message
        """
        request_json = request.json
        try:
            ShopProductService.insert_shop_products(
                db.engine, request_json
            )
        except ValidationError as error:
            return {'message': str(error)}, 400
        return {'message': 'Ok'}, 201

    def patch(self, instance_id):
        """
        Updates the shop product instance which shop id is instance_id
        and product id is passed as parameter product_id using
        the fields, passed into request body.
        :param instance_id: resource identificator to get a specific
                            shop product instance
        :return: if the correct data passed, a response with
                 the new instance info will be returned;
                 otherwise, a response body will contain an
                 error message
        """
        product_id = request.args.get('product_id')
        request_json = request.json
        try:
            ShopProductService.update_shop_products(
                db.session, instance_id, product_id, request_json
            )
        except ValidationError as error:
            return {'message': str(error)}, 400
        return {'message': 'Ok'}, 200

    def delete(self, instance_id=None):
        """
        Deletes the shop product instance which shop id is instance_id
        and product id is passed as parameter product_id.
        :param instance_id: resource identificator to get a specific
                            shop product instance
        :return: a response object
        """
        product_id = request.args.get('product_id')
        try:
            ShopProductService.delete_shop_product(
                db.engine, instance_id, product_id
            )
        except ValidationError as error:
            return {'message': str(error)}, 400
        return {'message': 'Ok'}, 204
