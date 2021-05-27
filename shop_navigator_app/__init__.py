from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from shop_navigator_app.config import DevelopmentConfig
from flask_cors import CORS

app = Flask(__name__)
app.debug = True
CORS(app)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

from shop_navigator_app.models import product
from shop_navigator_app.routes import routes_registering_list
