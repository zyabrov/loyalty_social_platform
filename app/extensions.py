from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_login import LoginManager
login_manager = LoginManager()

from instagram.client import InstagramAPI
# configure Instagram API

import requests

