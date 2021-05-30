"""
Provides tools to work with shop products table using ORM.
"""

from shop_navigator_app.models.shop import shops_products
from shop_navigator_app.models.product import Product


class ShopProductService:
    """
    Provides methods for executing CRUD operation in the
    database with shop products table and retrieving information from it.
    """

    @staticmethod
    def get_shop_products(session, instance_id, conditions):
        """
        :param session: establishes all conversations with the database
                        and represents a “holding zone” for all the
                        objects which you’ve loaded or associated with
                        it during its lifespan
        :param instance_id: resource identificator to get a specific
                            shop instance
        :param conditions: the conditions that table entities must satisfy
        :return: the table entities that satisfy the passed conditions
        """
        return session.query(
            shops_products.columns.product_id,
            shops_products.columns.price,
            shops_products.columns.count,
            Product.name
        ).select_from(
            shops_products.join(
                Product, Product.id == shops_products.columns.product_id
            )
        ).filter(
            shops_products.columns.shop_id == instance_id, *conditions
        ).all()

    @staticmethod
    def insert_shop_products(db_engine, shop_product_data):
        """
        Inserts a new shop product into the corresponding table
        :param db_engine: the database engine designed for query execution
        :param shop_product_data: a new shop product
        """
        query = shops_products.insert().values(shop_product_data)
        db_engine.execute(query)

    @staticmethod
    def update_shop_products(session, shop_id, product_id, updated_data):
        """
        :param session: establishes all conversations with the database
                        and represents a “holding zone” for all the
                        objects which you’ve loaded or associated with
                        it during its lifespan
        :param shop_id: the shop identificator
        :param product_id: the product in the passed shop identificator
        :param updated_data: new data about shop product that must replace
                             the old one
        """
        session.query(shops_products).filter(
            shops_products.c.shop_id == shop_id,
            shops_products.c.product_id == product_id
        ).update(updated_data)
        session.commit()

    @staticmethod
    def delete_shop_product(db_engine, shop_id, product_id):
        """
        Deletes the product that is in the passed store.
        :param db_engine: the database engine designed for query execution
        :param shop_id: the shop identificator
        :param product_id: the product in the passed shop identificator
        """
        query = shops_products.delete().where(
            shops_products.c.shop_id == shop_id,
            shops_products.c.product_id == product_id
        )
        db_engine.execute(query)
