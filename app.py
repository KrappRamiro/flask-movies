import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5b3cd5b80eb8b217c20fb37074ff4a33'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///default.db'

if 'RDS_DB_NAME' in os.environ:
    print("using the os.environ db")
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://{username}:{password}@{host}:{port}/{database}'.format(
        username=os.environ['RDS_USERNAME'],
        password=os.environ['RDS_PASSWORD'],
        host=os.environ['RDS_HOSTNAME'],
        port=os.environ['RDS_PORT'],
        database=os.environ['RDS_DB_NAME'],
    )
else:
    print("using the else db")
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://{username}:{password}@{host}:{port}/{database}'.format(
        username='flask-movies',
        password='complexpassword123',
        host='localhost',
        port='5432',
        database='flask-movies',
    )


db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    release_date = db.Column(db.Date(), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<Movie %r>' % self.title


@app.route('/')
def index():
    return 'flask-movies'


@app.route('/api/movies')
def api_movies():
    json = [movie.as_dict() for movie in Movie.query.all()]
    return jsonify(json)


if __name__ == '__main__':
    app.run(debug=True)
