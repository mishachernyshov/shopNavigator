from shop_navigator_app.schemas.shop_schema import ShopSchema
from shop_navigator_app.service.shop_service import ShopService
from shop_navigator_app.models.shop import Shop
from .base_view import BaseView


class ShopView(BaseView):
    def __init__(self):
        super().__init__(Shop, ShopSchema, ShopService)
