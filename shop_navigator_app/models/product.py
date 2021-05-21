from shop_navigator_app import db


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    rating = db.Column(db.Integer(), nullable=False)
    label = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        return self.name
