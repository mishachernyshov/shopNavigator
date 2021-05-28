from shop_navigator_app.models.shop import shops_products
from shop_navigator_app.models.product import Product


class ShopProductService:
    @staticmethod
    def get_shop_products(session, id, conditions):
        return session.query(
            shops_products.columns.product_id,
            shops_products.columns.price,
            shops_products.columns.count,
            Product.name
        ).select_from(
            shops_products.join(
                Product, Product.id == shops_products.columns.product_id
            )
        ).filter(shops_products.columns.shop_id == id, *conditions).all()

    @staticmethod
    def insert_shop_products(db_engine, shop_product_data):
        query = shops_products.insert().values(shop_product_data)
        db_engine.execute(query)

    @staticmethod
    def update_shop_products(session, id, product_id, updated_data):
        session.query(shops_products).filter(
            shops_products.c.shop_id == id,
            shops_products.c.product_id == product_id
        ).update(updated_data)
        session.commit()

    @staticmethod
    def delete_shop_product(db_engine, id, product_id):
        query = shops_products.delete().where(
            shops_products.c.shop_id == id,
            shops_products.c.product_id == product_id
        )
        db_engine.execute(query)
