"""
Stores the information about the products database table.
"""

from shop_navigator_app import db


class Product(db.Model):
    """
    Defines the products database table fields, constrains and
    functions to work with this model using ORM.
    """

    __tablename__ = 'products'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    rating = db.Column(db.Integer(), nullable=False)
    label = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        return self.name
