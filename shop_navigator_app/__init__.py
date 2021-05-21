from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Xpohuc490@localhost:5432/shop_db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

from shop_navigator_app.models import product
from shop_navigator_app.routes import routes_registering_list
