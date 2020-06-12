from app import app, db, bcrypt
from app.models.cats import Cats
from app.models.user import User
from app.models.people import Person
from flask import render_template, url_for, flash, redirect, request
from app.forms.forms import (
    LoginForm, RegistrationForm, UpdateAccountForm, RequestResetForm,
    ResetPasswordForm
)
from app.exceptions import InvalidPasswordException, InvalidEmailException
from flask_login import current_user, login_required
import os

@app.route('/health')
@app.route('/')
def health():
    """."""
    # return '<h1>health</h1>'
    raise Exception(app.root_path)


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
            next_page = request.args.get('next')

            if next_page:
                return redirect(url_for(next_page[1:]))

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


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    """."""
    User.log_out()
    return redirect(url_for('home'))


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    """."""
    image_file = url_for(
        'static',
        filename='profile_pics/{}'.format(current_user.image_file)
    )
    form = UpdateAccountForm()

    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    if form.validate_on_submit():
        try:
            if form.picture.data:
                User.save_profile_picture(
                    picture_file_data=form.picture.data,
                    picture_pre_path=os.path.join(app.root_path, 'static/profile_pics'),
                    user_id=current_user.user_id
                )
                image_file = url_for(
                    'static',
                    filename='profile_pics/{}'.format(current_user.image_file)
                )
            User.update_user(
                previous_username=current_user.username,
                new_username=form.username.data,
                new_email=form.email.data
            )
            flash('Account updated successfully.', 'success')

        except Exception as error:
            flash(str(error), 'danger')

    return render_template(
        'account.html', title='account', image_file=image_file, form=form
    )


@app.route('/request-password-update', methods=['POST', 'GET'])
def request_password_reset():
    """."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        try:
            user = User.get_by_email(email=form.email.data)
            User.send_password_update_email(
                user=user
            )
            flash(
                'An Email sent by the instructions to change the password',
                'success'
            )
            return redirect(url_for('login'))

        except InvalidEmailException as error:
            flash(str(error), 'danger')
    return render_template('request_password_update.html', form=form)


@app.route('/reset-password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    """."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token=token)
    if user:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.password = (
                bcrypt.generate_password_hash(form.password.data).decode(
                    'utf-8'
                )
            )
            db.session.commit()
            flash('Password changed successfully for the user.', 'success')
            return redirect(url_for('login'))

        return render_template('reset_password.html', form=form)
    else:
        flash('The token is not valid or expired.', 'danger')
        return redirect(url_for('request_password_reset'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
