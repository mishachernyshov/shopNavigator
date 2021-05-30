"""
Contains tools for executing CRUD operations with shops
and selecting information about shop entities by users via APIs.
"""

from shop_navigator_app.schemas.shop_schema import ShopSchema
from shop_navigator_app.service.shop_service import ShopService
from shop_navigator_app.models.shop import Shop
from .base_view import BaseView


class ShopView(BaseView):
    """
    Contains methods for getting HTTP-requests and sending HTTP-responses
    to provide APIs to work with the shop model.
    """

    def __init__(self):
        super().__init__(Shop, ShopSchema, ShopService)
