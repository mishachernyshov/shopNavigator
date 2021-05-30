"""
Provides tools to work with shop entities using ORM.
"""

from shop_navigator_app.models.shop import Shop
from shop_navigator_app.service.base_service import BaseService


class ShopService(BaseService):
    """
    Provides methods for executing CRUD operation in the
    database with shops table and retrieving information from it.
    """

    def __init__(self):
        super().__init__(Shop)

    @staticmethod
    def get_shop_name(session, instance_id):
        """
        :param session: establishes all conversations with the database
                        and represents a “holding zone” for all the
                        objects which you’ve loaded or associated with
                        it during its lifespan
        :param instance_id: resource identificator to get a specific
                            shop instance
        :return: the name of the shop that have the specified identificator
        """
        return session.query(Shop.name)\
            .filter(Shop.id == instance_id).first()[0]
