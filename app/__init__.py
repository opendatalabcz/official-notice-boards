from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap = Bootstrap5(app)
    # logging.basicConfig(level=logging.INFO)

    register_routes(app)
    return app


def register_routes(app: Flask):
    from app import routes
    app.add_url_rule('/', view_func=routes.view_index)
    app.add_url_rule('/municipalities', view_func=routes.view_municipalities)
    app.add_url_rule('/municipalities/<int:municipality_ruian>', view_func=routes.view_municipality)
    app.add_url_rule('/boards', view_func=routes.view_boards)
    app.add_url_rule('/boards/<int:board_id>', view_func=routes.view_board)
    app.add_url_rule('/notices', view_func=routes.view_notices)
    app.add_url_rule('/documents', view_func=routes.view_documents)
    # app.add_url_rule('/graphs', view_func=routes.view_graphs)
    # app.add_url_rule('/boards_experimental', view_func=routes.view_boards_experimental)
