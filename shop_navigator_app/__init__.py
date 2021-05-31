"""
The shop navigator application that provides APIs to manage
shops and products in them.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
import logging
import sys


def configure_logging():
    """
    Setting the logger configuration: where messages should be logged,
    what format they should have, the lowest logging level etc.
    """
    root_logger = logging.getLogger()

    log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)-5.5s]  %(message)s"
    )
    file_handler = logging.FileHandler("test.log")
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)

    logging.basicConfig(level=logging.DEBUG)


configure_logging()

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

from shop_navigator_app.routes import routes_registering_list
