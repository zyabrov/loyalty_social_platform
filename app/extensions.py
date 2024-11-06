from flask import current_app

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_login import LoginManager
login_manager = LoginManager()

from instagram.client import InstagramAPI
# configure Instagram API

from flask_migrate import Migrate

import requests

from geosky import geo_plug

