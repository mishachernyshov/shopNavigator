"""
Provides tools to get aggregated data about shops using ORM.
"""

from sqlalchemy import func

from shop_navigator_app.models.shop import Shop, shops_products
from shop_navigator_app.models.address import Address


class AggregatedShopsService:
    """
    Provides methods for collecting the aggregated data
    about shops from the database.
    """

    @staticmethod
    def get_aggregated_shops_list(session):
        """

        :param session: establishes all conversations with the database
                        and represents a “holding zone” for all the
                        objects which you’ve loaded or associated with
                        it during its lifespan
        :return: the aggregated data about shops such as product count
                 in them and the average product price
        """
        return session.query(
            Shop,
            Address,
            func.count(shops_products.columns.product_id)
            .label('product_count'),
            func.avg(shops_products.columns.price)
            .label('average_price')
        ).join(Address).outerjoin(shops_products).group_by(Shop, Address).all()
