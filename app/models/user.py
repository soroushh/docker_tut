from app import db, login_manager, bcrypt, app
from app.exceptions import (
    RepetitiveEmailException, RepetitiveUsernameException,
    InvalidEmailException, InvalidPasswordException
)
from flask_login import UserMixin, login_user, logout_user
import secrets
import os
from PIL import Image
from itsdangerous import TimedJSONWebSignatureSerializer as Serialiser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """."""
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg', nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # def __repr__(self):
    #     """."""
    #     return f'User({self.username},{self.email},{self.image})'

    @classmethod
    def create_user(cls, username, password, email):
        """."""
        rep_user_email = cls.query.filter_by(email=email).first()
        rep_user_username = cls.query.filter_by(username=username).first()

        if rep_user_email:
            raise RepetitiveEmailException(
                'The email is repetitive.'
            )
        if rep_user_username:
            raise RepetitiveUsernameException(
                'The username is repetitive.'
            )
        db.session.add(cls(username=username, email=email, password=password))
        db.session.commit()

    @classmethod
    def login(cls, email, password, remember):
        """Finds a user by a specific email and password and do the login."""
        user = cls.query.filter_by(email=email).first()

        if not user:
            raise InvalidEmailException('The email is invalid.')

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
        else:
            raise InvalidPasswordException('The password is invalid.')

    def get_id(self):
        """."""
        return self.user_id

    @staticmethod
    def log_out():
        """."""
        logout_user()

    @classmethod
    def update_user(
        cls,
        previous_username,
        new_username,
        new_email
    ):
        """."""
        current_user = cls.query.filter_by(username=previous_username).first()
        existing_user_with_new_email = cls.query.filter_by(email=new_email).first()
        existing_user_with_new_username = cls.query.filter_by(username=new_username).first()

        if existing_user_with_new_username and existing_user_with_new_username.user_id != current_user.user_id:
            raise RepetitiveUsernameException(
                'Another user has the new username you have chosen.'
            )

        if existing_user_with_new_email and existing_user_with_new_email.user_id != current_user.user_id:
            raise RepetitiveEmailException(
                'Another user has the new email you have chosen.'
            )

        current_user.username = new_username
        current_user.email = new_email
        db.session.commit()

    @classmethod
    def save_profile_picture(cls, user_id, picture_file_data, picture_pre_path):
        """."""
        user = cls.query.get(user_id)
        random_string = secrets.token_hex(8)
        useless, file_extension = os.path.splitext(picture_file_data.filename)
        file_name = random_string + file_extension
        picture_final_path = os.path.join(picture_pre_path, file_name)

        output_size = (125, 125)
        image = Image.open(picture_file_data)
        image.thumbnail(output_size)
        image.save(picture_final_path)

        user.image_file = file_name
        db.session.commit()

        return file_name

    def get_reset_token(self, expires_sec=1800):
        """Creates a timed json token.

        The expiry duration time of the token is 1800 seconds which is half an
        hour.
        """
        s = Serialiser(app.config['SECRET_KEY'], expires_sec)

        return s.dump({'user_id': self.user_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """Receives a token and verifies if it is valid.

        If the token is valid, we will get the user_id of the user which has
        forgotten the password for logging in.
        """
        s = Serialiser(app.config['SECRET_KEY'])

        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        return User.query.get(user_id)

    @classmethod
    def get_by_email(cls, email):
        """Finds a user by the email."""
        user = cls.query.filter_by(email=email).first()
        if not user:
            raise InvalidEmailException(
                'The user with provided email does not exist.'
            )
        return user

    @classmethod
    def send_password_update_email(cls, payload):
        """."""
        pass
