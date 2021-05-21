from shop_navigator_app.schemas.address_schema import AddressSchema
from shop_navigator_app.models.address import Address
from .base_view import BaseView


class AddressView(BaseView):
    def __init__(self):
        super().__init__(AddressSchema, Address)
