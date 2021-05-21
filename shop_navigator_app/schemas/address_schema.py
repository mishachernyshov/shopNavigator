from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from shop_navigator_app.models.address import Address


class AddressSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Address
        load_instance = True
        include_fk = True
