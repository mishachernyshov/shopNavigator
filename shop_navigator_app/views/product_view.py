from shop_navigator_app.schemas.product_schema import ProductSchema
from shop_navigator_app.models.product import Product
from .base_view import BaseView


class ProductView(BaseView):
    def __init__(self):
        super().__init__(ProductSchema, Product)
