from shop_navigator_app.models.shop import Shop
from shop_navigator_app.service.base_service import BaseService


class ShopService(BaseService):
    def __init__(self):
        super().__init__(Shop)

    @staticmethod
    def get_shop_name(session, id):
        return session.query(Shop.name)\
            .filter(Shop.id == id).first()[0]
