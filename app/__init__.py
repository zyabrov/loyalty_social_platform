from flask import Flask


from config import Config
from app.extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.debug = True

    # Initialize Flask extensions here
    db.init_app(app)

    login_manager.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.users import bp as users_bp
    app.register_blueprint(users_bp)

    from app.bonuses import bp as bonuses_bp
    app.register_blueprint(bonuses_bp, url_prefix='/bonuses')

    from app.bonusactions import bp as bonusactions_bp
    app.register_blueprint(bonusactions_bp, url_prefix='/bonusactions')

    from app.bonuses_base import bp as bonuses_base_bp
    app.register_blueprint(bonuses_base_bp)

    from app.rewardactions import bp as rewardactions_bp
    app.register_blueprint(rewardactions_bp, url_prefix='/rewardactions')
    
    from app.certificates import bp as certificates_bp
    app.register_blueprint(certificates_bp, url_prefix='/certificates')

    from app.rewards import bp as rewards_bp
    app.register_blueprint(rewards_bp, url_prefix='/rewards')

    
    return app