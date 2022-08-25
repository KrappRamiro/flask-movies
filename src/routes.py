# This file is used for url routes
from src import app
from src import db
from flask import render_template, request, jsonify
from src.db_models import Movie
# Define the db model for the movies

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
