"""
Provides tools to work with shop entities using ORM.
"""

from shop_navigator_app.models.product import Product
from shop_navigator_app.service.base_service import BaseService


class ProductService(BaseService):
    """
    Provides methods for executing CRUD operation in the
    database with products table and retrieving information from it.
    """

    def __init__(self):
        super().__init__(Product)

    @staticmethod
    def get_main_info(session):
        """
        :param session: establishes all conversations with the database
                        and represents a “holding zone” for all the
                        objects which you’ve loaded or associated with
                        it during its lifespan
        :return: the main information such as id and name about all products
        """
        return session.query(
            Product.id, Product.name
        ).all()
