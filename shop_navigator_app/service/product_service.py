from shop_navigator_app.models.product import Product
from shop_navigator_app.service.base_service import BaseService


class ProductService(BaseService):
    def __init__(self):
        super().__init__(Product)

    @staticmethod
    def get_main_info(session):
        return session.query(
            Product.id, Product.name
        ).all()
