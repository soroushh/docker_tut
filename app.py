from models import app, db
from models.cats import Cats
from models.people import Person


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


@app.route('/create-person/<name>/<family>')
def create_person(name, family):
    """."""
    db.session.add(Person(name=name, family=family))
    db.session.commit()

    return f'The person:{name} {family} was created successfully.'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
