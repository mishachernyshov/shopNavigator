"""
Contains tools for executing CRUD operations with addresses
and selecting information about address entities by users via APIs.
"""

from shop_navigator_app.schemas.address_schema import AddressSchema
from shop_navigator_app.service.address_service import AddressService
from shop_navigator_app.models.address import Address
from .base_view import BaseView


class AddressView(BaseView):
    """
    Contains methods for getting HTTP-requests and sending HTTP-responses
    to provide APIs to work with the address model.
    """

    def __init__(self):
        super().__init__(Address, AddressSchema, AddressService)
