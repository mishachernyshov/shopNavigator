from flask_restful import Resource
from marshmallow import ValidationError

from shop_navigator_app.models.shop import shops_products
from shop_navigator_app.service.shop_product_service \
    import ShopProductService
from shop_navigator_app.service.shop_service import ShopService
from flask import request
from shop_navigator_app.schemas.shop_products_schema \
    import ShopProductsSchema

from shop_navigator_app import db


class ShopProductsView(Resource):
    def get(self, id=None):
        if not id:
            return {}, 404
        min_price, max_price, exact_price = self.get_params(request.args)
        conditions = self.get_conditions(exact_price, min_price, max_price)
        shop_name = ShopService.get_shop_name(db.session, id)
        shop_products = ShopProductService.get_shop_products(
            db.session, id, conditions
        )
        response = self.make_response(shop_name, shop_products)
        return response, 200

    def get_params(self, request_arguments):
        min_price = request_arguments.get('min_price')
        max_price = request_arguments.get('max_price')
        exact_price = request_arguments.get('exact_price')

        return min_price, max_price, exact_price

    def get_conditions(self, exact_price, min_price, max_price):
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

    def make_response(self, shop_name, shop_products):
        return {
            'name': shop_name,
            'products': ShopProductsSchema().dump(shop_products, many=True)
        }

    def post(self):
        request_json = request.json
        try:
            ShopProductService.insert_shop_products(
                db.engine, request_json
            )
        except ValidationError as e:
            return {'message': str(e)}, 400
        return {'message': 'Ok'}, 201

    def patch(self, id):
        product_id = request.args.get('product_id')
        request_json = request.json
        try:
            ShopProductService.update_shop_products(
                db.session, id, product_id, request_json
            )
        except ValidationError as e:
            return {'message': str(e)}, 400
        return {'message': 'Ok'}, 200

    def delete(self, id=None):
        product_id = request.args.get('product_id')
        try:
            ShopProductService.delete_shop_product(
                db.engine, id, product_id
            )
        except ValidationError as e:
            return {'message': str(e)}, 400
        return {'message': 'Ok'}, 204
