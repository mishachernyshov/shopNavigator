from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS


app = Flask(__name__)
app.debug = True
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Xpohuc490@localhost:5432/shop_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

if __name__ == '__main__':
    app.run()

from shop_navigator_app.models import product
from shop_navigator_app.routes import routes_registering_list
