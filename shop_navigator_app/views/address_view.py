from shop_navigator_app.schemas.address_schema import AddressSchema
from shop_navigator_app.service.address_service import AddressService
from .base_view import BaseView


class AddressView(BaseView):
    def __init__(self):
        super().__init__(AddressSchema, AddressService)
