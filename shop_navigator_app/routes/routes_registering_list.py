"""
Specifies the endpoints that clients can use to make HTTP requests
and get responses from the server.
"""

from shop_navigator_app.views.address_view import AddressView
from shop_navigator_app.views.shop_products_view \
    import ShopProductsView
from shop_navigator_app.views.products_main_info_view \
    import ProductsMainInfoView
from shop_navigator_app.views.shop_view import ShopView
from shop_navigator_app.views.product_view import ProductView
from shop_navigator_app.views.aggregated_shops_view \
    import AggregatedShopsView
from shop_navigator_app import api

api.add_resource(
    AddressView, '/address', '/address/<instance_id>',
    strict_slashes=False
)
api.add_resource(
    ShopView, '/shop', '/shop/<instance_id>',
    strict_slashes=False
)
api.add_resource(
    ProductView, '/product', '/product/<instance_id>',
    strict_slashes=False
)
api.add_resource(
    AggregatedShopsView, '/aggregated_shops',
    strict_slashes=False
)
api.add_resource(
    ShopProductsView, '/shop_products',
    '/shop_products/<instance_id>', strict_slashes=False
)
api.add_resource(
    ProductsMainInfoView, '/products_main_info',
    strict_slashes=False
)
