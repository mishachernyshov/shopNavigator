from shop_navigator_app.views.address_view import AddressView
from shop_navigator_app.views.shop_view import ShopView
from shop_navigator_app.views.product_view import ProductView
from shop_navigator_app import api

api.add_resource(AddressView, '/address', '/address/<id>', strict_slashes=False)
api.add_resource(ShopView, '/shop', '/shop/<id>', strict_slashes=False)
api.add_resource(ProductView, '/product', '/product/<id>', strict_slashes=False)
