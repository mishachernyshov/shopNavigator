from flask_restful import Resource
from marshmallow import ValidationError

from shop_navigator_app.models.shop import Shop, shops_products
from shop_navigator_app.models.product import Product
from flask import request
from shop_navigator_app.schemas.shop_products_schema \
    import ShopProductsSchema

from .. import db


class ShopProductsView(Resource):
    def get(self, id=None):
        if not id:
            return {}, 404
        min_price, max_price, exact_price = self.get_params(request.args)
        conditions = self.get_conditions(exact_price, min_price, max_price)
        shop_name = self.get_shop_name(id)
        shop_products = self.get_shop_products(id, conditions)
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

    def get_shop_products(self, id, conditions):
        return db.session.query(
            shops_products.columns.product_id,
            shops_products.columns.price,
            shops_products.columns.count,
            Product.name
        ).select_from(
            shops_products.join(
                Product, Product.id == shops_products.columns.product_id
            )
        ).filter(shops_products.columns.shop_id == id, *conditions).all()

    def get_shop_name(self, id):
        return db.session.query(Shop.name).filter(Shop.id == id).first()[0]

    def make_response(self, shop_name, shop_products):
        return {
            'name': shop_name,
            'products': ShopProductsSchema().dump(shop_products, many=True)
        }

    def post(self):
        request_json = request.json
        query = shops_products.insert().values(request_json)
        try:
            db.engine.execute(query)
        except ValidationError as e:
            return {'message': str(e)}, 400
        return {'message': 'Ok'}, 201

    def patch(self, id):
        product_id = request.args.get('product_id')
        request_json = request.json
        try:
            db.session.query(shops_products).filter(
                shops_products.c.shop_id == id,
                shops_products.c.product_id == product_id
            ).update(request_json)
            db.session.commit()
        except ValidationError as e:
            return {'message': str(e)}, 400
        return {'message': 'Ok'}, 200

    def delete(self, id=None):
        product_id = request.args.get('product_id')
        query = shops_products.delete().where(
            shops_products.c.shop_id == id,
            shops_products.c.product_id == product_id
        )
        try:
            db.engine.execute(query)
        except ValidationError as e:
            return {'message': str(e)}, 400
        return {'message': 'Ok'}, 204
