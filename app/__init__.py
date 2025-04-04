from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import config_by_name

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.webhooks import webhook
    app.register_blueprint(webhook, url_prefix='/')

    return app