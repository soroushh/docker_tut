from flask import Flask
import redis
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefgh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://test:password@postgres:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

cache = redis.Redis(host='redis', port=6379)
