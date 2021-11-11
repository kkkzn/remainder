from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

from remainder.config import Config
from remainder.main.utils import simplify


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    # Custom filter
    app.jinja_env.filters["simplify"] = simplify

    from remainder.users.routes import users_bp
    from remainder.records.routes import records_bp
    from remainder.main.routes import main_bp
    from remainder.errors.handlers import errors_bp
    app.register_blueprint(users_bp)
    app.register_blueprint(records_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)

    return app
