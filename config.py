import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'b16cfd0745a12beca24a3e108ad9bc17' #os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    INSTAGRAM_CLIENT_ID = 722187390079358 #os.environ.get('CLIENT_ID')
    INSTAGRAM_CLIENT_SECRET = 'f6bfdb605aea9675c82f047411c94019' #os.environ.get('CLIENT_SECRET')
