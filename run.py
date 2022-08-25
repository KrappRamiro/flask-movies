import os
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5b3cd5b80eb8b217c20fb37074ff4a33'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the database URI
if 'RDS_DB_NAME' in os.environ:
    print("using the ElasticBeanstalk db")
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://{username}:{password}@{host}:{port}/{database}'.format(
        username=os.environ['RDS_USERNAME'],
        password=os.environ['RDS_PASSWORD'],
        host=os.environ['RDS_HOSTNAME'],
        port=os.environ['RDS_PORT'],
        database=os.environ['RDS_DB_NAME'],
    )
else:
    print("using the local postgresql db")
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://{username}:{password}@{host}:{port}/{database}'.format(
        username='flask-movies',
        password='complexpassword123',
        host='localhost',
        port='5432',
        database='flask-movies',
    )

db = SQLAlchemy(app)


# Define the db model for the movies
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    release_date = db.Column(db.Date(), nullable=False)

    # Return a list of all the movies as a dictionary
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<Movie %r>' % self.title


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/data', methods=["POST", "GET"])
def data():
    if request.method == "GET":
        return f"The URL /data was accesed directly. This is not valid, try going to /form to submit form, and that will redirect you to /data"
    if request.method == "POST":
        form_data = request.form
        return render_template('data.html', form_data=form_data)


@app.route('/api/movies')
def api_movies():
    json = [movie.as_dict() for movie in Movie.query.all()]
    return jsonify(json)


if __name__ == '__main__':
    app.run(debug=True)
