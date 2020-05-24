from app import db


class Person(db.Model):
    """Definition of a person."""
    __tablename__ = 'people'
    person_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    family = db.Column(db.String(20))
