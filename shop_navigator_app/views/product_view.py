from shop_navigator_app.schemas.product_schema import ProductSchema
from shop_navigator_app.service.product_service import ProductService
from .base_view import BaseView


class ProductView(BaseView):
    def __init__(self):
        super().__init__(ProductSchema, ProductService)
