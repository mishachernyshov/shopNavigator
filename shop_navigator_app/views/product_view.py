from shop_navigator_app.schemas.product_schema import ProductSchema
from shop_navigator_app.service.product_service import ProductService
from shop_navigator_app.models.product import Product
from .base_view import BaseView
from sqlalchemy import inspect


class ProductView(BaseView):
    def __init__(self):
        super().__init__(Product, ProductSchema, ProductService)

    def check_instance_data(self, request_data):
        if current_rating := request_data.get('rating'):
            if not 1 <= current_rating <= 5:
                return False

        product_column_set = set(inspect(Product).column_attrs.keys())
        product_column_set.remove('id')
        given_column_set = set(request_data.keys())
        if product_column_set == given_column_set:
            return True
        product_column_set.remove('label')
        return product_column_set == given_column_set
