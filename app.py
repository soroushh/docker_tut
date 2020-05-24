from flask import Flask
import redis
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://test:password@postgres:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

cache = redis.Redis(host='redis', port=6379)


class Cats(db.Model):
    __tablename__ = 'cats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer, default=1000)
    breed = db.Column(db.String(100))


class Person(db.Model):
    """Definition of a person."""
    __tablename__ = 'people'
    person_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    family = db.Column(db.String(20))


@app.route('/health')
@app.route('/')
def health():
    """."""
    return 'health'


@app.route('/create-cat/<name>/<breed>')
def create_cat(name, breed):
    """."""
    db.session.add(Cats(name=name, breed=breed))
    db.session.commit()

    return f'The cat: {name} with the breed:{breed} is created successfully.'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

