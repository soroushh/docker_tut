from flask import Flask
import redis
import sys
import time
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from app_conf import DATABASE_CONNECTION_URI
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://test:password@postgres:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)
# db.create_all()

cache = redis.Redis(host='redis', port=6379)


def print_psycopg2_exception(err):
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno


class Cats(db.Model):
    __tablename__ = 'cats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    breed = db.Column(db.String(100))


class Person(db.Model):
    """Definition of a person."""
    __tablename__ = 'people'
    person_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    family = db.Column(db.String(20))


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    db.create_all()
    db.session.add(Cats(name='soroush', price=1000, breed='German'))
    db.session.commit()
    return 'Cat soroush successfully saved.'


@app.route('/show_cats')
def show():
    cat = Cats.query.filter_by(name ='soroush').first()
    return cat.name


@app.route('/create_cat/<string:name>/<string:breed>/<int:price>/<pname>/<family>')
def create_cat(name, breed, price, pname, family):
    """."""
    try:
        create_cat(name=name, breed=breed, price=price, commit=False)
        raise Exception('An error was raised')
    except Exception:
        create_person(name=pname, family=family)
        return 'Committed after raising an error.'

    return f'Cat named {name} with breed {breed} was created successfully.'


@app.route('/commit')
def commit():
    """."""
    db.session.commit()
    return 'abc'


@app.route('/drop-all')
def drop_all_tables():
    """."""
    db.drop_all()
    return "All tables removed and recreated successfully."


@app.route('/health')
def health():
    """."""
    return 'health'


def create_cat(name, price, breed, commit=True):
    """."""
    db.session.add(Cats(name=name, breed=breed, price=price))
    if commit:
        db.session.commit()
    else:
        db.session.flush()

def create_person(name, family):
    """."""
    db.session.add(Person(name=name, family=family))
    db.session.commit()





if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

