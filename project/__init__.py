from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = os.environ.get('SECRET_KEY')
    db.init_app(app)
    
    from project.views.index import main
    app.register_blueprint(main)
    
    from project.views.booking import booking
    app.register_blueprint(booking, url_prefix='/booking')
    
    return app