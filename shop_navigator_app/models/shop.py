"""
Stores the information about the shops database table.
"""

from shop_navigator_app import db
from shop_navigator_app.models.product import Product

shops_products = db.Table(
    'shops_products',
    db.Column('shop_id', db.Integer(), db.ForeignKey('shops.id'), primary_key=True),
    db.Column('product_id', db.Integer(), db.ForeignKey('products.id'), primary_key=True),
    db.Column('price', db.DECIMAL(), nullable=False),
    db.Column('count', db.Integer(), nullable=False)
)


class Shop(db.Model):
    """
    Defines the shops database table fields, constrains and
    functions to work with this model using ORM.
    """

    __tablename__ = 'shops'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    address_id = db.Column(
        db.Integer(),
        db.ForeignKey('addresses.id', ondelete='CASCADE'),
        nullable=False
    )
    about = db.Column(db.Text(), nullable=False)
    products = db.relationship(
        'Product', secondary=shops_products, lazy='subquery',
        backref=db.backref('shops', lazy=True)
    )

    def __repr__(self):
        return f'{self.name} ({self.address})'
