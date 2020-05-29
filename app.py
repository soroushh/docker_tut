from app import app, db, bcrypt
from app.models.cats import Cats
from app.models.user import User
from app.models.people import Person
from flask import render_template, url_for, flash, redirect
from app.forms.forms import LoginForm, RegistrationForm
from app.exceptions import InvalidPasswordException, InvalidEmailException
from flask_login import current_user


@app.route('/health')
@app.route('/')
def health():
    """."""
    return '<h1>health</h1>'


@app.route('/home')
def home():
    """."""
    return render_template('home.html')


@app.route('/about')
def about():
    """."""
    return render_template('about.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    """."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            User.create_user(
                username=form.username.data,
                password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
                email=form.email.data
            )
            flash(
                f' The user:{form.username.data} is created.',
                f'success'
            )
            return redirect(url_for('login'))
        except Exception as exec:
            flash(
                str(exec),
                'danger'
            )

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    """."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            User.login(
                email=form.email.data,
                password=form.password.data,
                remember=form.remember.data
            )

            flash(
                'Successfully logged in.',
                'success'
            )
            return redirect(url_for('home'))

        except InvalidPasswordException as error:
            flash(
                str(error),
                'danger'
            )

        except InvalidEmailException as error:
            flash(
                str(error),
                'danger'
            )

    return render_template('login.html', title='Login', form=form)


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


@app.route('/create-user/<username>/<email>/<password>')
def create_user(username, email, password):
    """."""
    db.session.add(User(
        username=username,
        email=email,
        password=password
    ))
    db.session.commit()

    return f'The username:{username} was created successfully.'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
