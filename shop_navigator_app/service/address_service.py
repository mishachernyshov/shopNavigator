from shop_navigator_app.models.address import Address
from shop_navigator_app.service.base_service import BaseService


class AddressService(BaseService):
    def __init__(self):
        super().__init__(Address)
