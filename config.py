import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'b16cfd0745a12beca24a3e108ad9bc17' #os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    INSTAGRAM_CLIENT_ID = 722187390079358 #os.environ.get('CLIENT_ID')
    INSTAGRAM_CLIENT_SECRET = 'f6bfdb605aea9675c82f047411c94019' #os.environ.get('CLIENT_SECRET')
    UPLOAD_FOLDER = os.path.join(basedir, 'app','static', 'uploads')
    BOT_TOKEN = '7434147333:AAGamjeLO4OleLl8xesYecOx6-ezqGyQ-wI'#os.environ.get('BOT_TOKEN')
    BOT_URL = 'https://t.me/rationallife_bot'
    WEBAPP_URL = 'https://rationallife.pythonanywhere.com'
    WEBHOOK_URL = f'{WEBAPP_URL}/tg_bot/'
    SHOPS_UPLOAD_DIR = os.path.join(basedir, 'app', 'static', 'uploads', 'shops')
    TEMP_UPLOAD_DIR = os.path.join(basedir, 'app', 'static', 'uploads', 'temp')
    USERS_UPLOAD_DIR = os.path.join(basedir, 'app', 'static', 'uploads', 'users')

    CRYPTOMUS_API = 'oS7PyppjpJLxysTnF7qXNMwaX4N6SbArd92dg7GGLYavK25tdDEvzNE2KAo5d8akEgQQ9flQRThxvJYZS9wbeP9CTqt7kBzgwI06o0ziyeZzmhvBvGbxOzAy2jxzsWQO'
    OPENAI_API_KEY = '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'

    INSTAGRAM_API_SECRET = '511181c5c581e27c0b7603cf5fffa923'
    INSTAGRAM_API_ID = 397536966768110
    INSTAGRAM_API_NAME = 'Rational Life App'
    INSTAGRAM_API_TOKEN = 'EAAFpjsmwde4BOyPcnZC21nBPaWdMZCNlyZAi32smMkZBZBRT5GufnVqF3awLXCWuDPe95A2uwHaCxGuOKs7uawOpqZApsUk1VSrsNzwt8QEdoTMjQXbztXz0rCZBZAvWqAn71vBDhOrO7SWkN0qEaPzl04AKw3B2IIN3VkWuAF56WQvtCZB1z70Y6xVgbLbr2YUYQLAmtgpwwb9fxT0BxJbEZD'
    INSTAGRAM_API_URL = 'https://graph.facebook.com/v21.0/'
    # INSTAGRAM_ACCESS_MARKER = 'XIGQWROU1dfSHNtRGlPbGY0NndwdUhNcUlyOGRaWEo2dFBHbURqQnBCVnY2ejh5ZAHdWVDN5ZAUhtcHRvNU82anI5SmEzQ1BXVUpsOHVZAOTBTVkpwbXFPNmNnVm5qZADdVbWg5dXV0Nkl3T3FJMEpzRWczZAklMMHRPTzAZD'
    INSTAGRAM_ACCESS_MARKER = 'IGQWROM0xsN21MdldQMUNnYllGVkczeXdIQWc2VHUyQVRyRDRSNkZAmRlpjbm9Lam5LTFlRcGN6cnJkMHNKNlFNLXdMTWZAxTkpqaFctTXFHT1A0cGFIWExtdDdnRmtrNTFTVHZAqcGtYLWhRSXlWVjNoWDJjdlBsancZD'
    INSTAGRAM_APP_CLIENT_ID = 1624464474776380
    INSTAGRAM_LOGIN_REDIRECT_URL = WEBAPP_URL + '/instagram/webhook'
    # INSTAGRAM_LOGIN_URL = f'https://www.instagram.com/oauth/authorize?client_id={INSTAGRAM_APP_CLIENT_ID}&redirect_uri={INSTAGRAM_LOGIN_REDIRECT_URL}/&response_type=code&scope=business_basic%2Cbusiness_manage_messages%2Cbusiness_manage_comments%2Cbusiness_content_publish
    # comments, live_comments, message_reactions, messages, messaging_optins, messaging_postbacks, messaging_referral и messaging_seen