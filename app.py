from app import app, db
from app.cats import Cats
from app.people import Person
from flask import render_template


@app.route('/health')
@app.route('/')
def health():
    """."""
    return '<h1>health</h1>'


@app.route('/home')
def home():
    """."""
    return render_template('home.html')


@app.route('/create-cat/<name>/<breed>')
def create_cat(name, breed):
    """."""
    db.session.add(Cats(name=name, breed=breed))
    db.session.commit()

    return f'The cat: {name} with the breed:{breed} is created successfully.'


@app.route('/create-person/<name>/<family>')
def create_person(name, family):
    """."""
    db.session.add(Person(name=name, family=family))
    db.session.commit()

    return f'The person:{name} {family} was created successfully.'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
