from shop_navigator_app import db
from shop_navigator_app.models.shop import Shop


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer(), primary_key=True)
    country = db.Column(db.String(25), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    street = db.Column(db.String(30), nullable=False)
    building = db.Column(db.String(5), nullable=False)
    shops = db.relationship('Shop', backref='address', passive_deletes=True)

    def __repr__(self):
        return f'Address: {self.country}, {self.city}, {self.street}, {self.building}'
