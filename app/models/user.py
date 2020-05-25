from app import db
from app.exceptions import (
    RepetitiveEmailException, RepetitiveUsernameException
)


class User(db.Model):
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


