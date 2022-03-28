from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bootstrap = Bootstrap5(app)
    # logging.basicConfig(level=logging.INFO)

    register_routes(app)
    return app


def register_routes(app: Flask):
    from app import routes
    app.add_url_rule('/', view_func=routes.index)
    app.add_url_rule('/municipalities', view_func=routes.view_municipalities)
    app.add_url_rule('/boards', view_func=routes.view_boards)
    app.add_url_rule('/boards/<int:board_id>', view_func=routes.view_board)
    app.add_url_rule('/notices', view_func=routes.view_notices)
    app.add_url_rule('/documents', view_func=routes.view_documents)
    app.add_url_rule('/graphs', view_func=routes.view_graphs)

