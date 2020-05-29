from app import db, login_manager, bcrypt
from app.exceptions import (
    RepetitiveEmailException, RepetitiveUsernameException,
    InvalidEmailException, InvalidPasswordException
)
from flask_login import UserMixin, login_user


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

    def __repr__(self):
        """."""
        return f'User({self.username},{self.email},{self.image})'

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
        """Finds a user by a specific email and password."""
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




