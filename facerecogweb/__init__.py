import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)
    #app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://cpedev@localhost/cpedb"
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #db = SQLAlchemy(app)
    app.secret_key = 'mamamo'
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import (index, admin)
    app.register_blueprint(index.bp)
    app.register_blueprint(admin.bp)
    
    return app
