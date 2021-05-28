from shop_navigator_app.models.shop import Shop, shops_products
from shop_navigator_app.models.address import Address
from sqlalchemy import func


class AggregatedShopsService:
    @staticmethod
    def get_aggregated_shops_list(session):
        return session.query(
            Shop,
            Address,
            func.count(shops_products.columns.product_id)
            .label('product_count'),
            func.avg(shops_products.columns.price)
            .label('average_price')
        ).join(Address).outerjoin(shops_products).group_by(Shop, Address).all()
