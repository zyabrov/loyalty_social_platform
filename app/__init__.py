from flask import Flask
import logging
from config import Config
from app.extensions import db, login_manager
from flask_migrate import Migrate


def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(config_class)
    app.debug = True
    
    # Initialize Flask extensions here
    db.init_app(app)
    migrate = Migrate(app, db)
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'migrate': migrate}

    logging.basicConfig()
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    login_manager.init_app(app)

    # Run db.create_all() when Flask runs
    with app.app_context():
        db.create_all()
        migrate.init_app(app, db)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.shops import bp as shops_bp
    app.register_blueprint(shops_bp, url_prefix='/shops')
    
    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from app.actions import bp as actions_bp
    app.register_blueprint(actions_bp, url_prefix='/actions')

    from app.tasks import bp as tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    from app.rewards import bp as rewards_bp
    app.register_blueprint(rewards_bp, url_prefix='/rewards')

    from app.admins import bp as admins_bp
    app.register_blueprint(admins_bp, url_prefix='/admins')

    from app.products import bp as products_bp
    app.register_blueprint(products_bp, url_prefix='/products')

    from app.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    from app.instagram import bp as instagram_bp
    app.register_blueprint(instagram_bp, url_prefix='/instagram')

    from app.notifications import bp as notifications_bp
    app.register_blueprint(notifications_bp, url_prefix='/notifications')

    from app.tg_bot import bp as tg_bot_bp
    app.register_blueprint(tg_bot_bp, url_prefix='/tg_bot')

    from app.payments import bp as payments_bp
    app.register_blueprint(payments_bp, url_prefix='/payments')
    
    
    return app