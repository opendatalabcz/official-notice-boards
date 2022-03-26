import logging

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:example@localhost:5432/postgres'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/postgres'
# app.config['PAS']
# TODO replace by env var, either .env file or in docker-compose
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///official_notice_boards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'Flatly'

db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)
logging.basicConfig(level=logging.INFO)

from src import views
app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/municipality', view_func=views.municipality)
app.add_url_rule('/board', view_func=views.board)
app.add_url_rule('/notice', view_func=views.notice)
app.add_url_rule('/document', view_func=views.document)

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
