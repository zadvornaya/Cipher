from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Пожалуйста, войдите, чтобы получить доступ к этой странице'
bootstrap = Bootstrap()


# security = Security()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)

    # Flask security
    # from app.models import Role, User
    # user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    # security.init_app(app, user_datastore)

    # Blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp, url_prefix='/error')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.post import bp as post_bp
    app.register_blueprint(post_bp, url_prefix='/posts')

    return app


from app import models
