from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.config import Config

# Initialise Flask extensions
db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Configuration settings
    app.config.from_object(Config)

    # Initialise extensions
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    # Import blueprints
    from app.routes import main_bp
    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.articles.routes import articles_bp
    from app.blueprints.courses.routes import courses_bp
    from app.blueprints.events.routes import events_bp
    from app.blueprints.admin.routes import admin_bp

    # Register routes
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(articles_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(admin_bp)

    return app
