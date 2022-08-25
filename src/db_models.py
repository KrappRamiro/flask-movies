# This file is used for database models
from src import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    release_date = db.Column(db.Date(), nullable=False)

    # Return a list of all the movies as a dictionary
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<Movie %r>' % self.title
