"""
Provides tools to work with address entities using ORM.
"""

from shop_navigator_app.models.address import Address
from shop_navigator_app.service.base_service import BaseService


class AddressService(BaseService):
    """
    Provides methods for executing CRUD operation in the
    database with addresses table and retrieving information from it.
    """

    def __init__(self):
        super().__init__(Address)
