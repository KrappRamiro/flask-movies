# This file is used for url routes
from src import app
from src import db
from flask import render_template, request, jsonify, redirect, url_for
from src.db_models import Movie
from src.forms import MovieForm


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

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie(): #A add_movie le pasan una request como parametro
    form = MovieForm() # la variable form va a instanciar al Form que tengo definido en forms.py
    if form.validate_on_submit():
        movie = Movie() # We instance the Movie class that is defined in db_models.py
        movie.release_date = form.release_date.data # We save the release date that is stored in the form
        movie.title = form.title.data # We save the title that is stored in the form
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('add_movie'))
    if form.errors != {}: #If there are errors
        for err_msg in form.errors.values():
            print("There was an error: \t {err_msg}")
    return render_template('add_movie.html', form=form)

@app.route('/see_movies', methods=['GET', 'POST'])
def see_movies():
    movies = Movie.query.all()
    return render_template('see_movies.html', movies=movies)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Movie.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('see_movies'))
    except:
        return 'There was a problem deleting that movie'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    movie = Movie.query.get_or_404(id)

    if request.method == 'POST':
        movie.title = request.form['title']
        print(movie.title)
        try:
            db.session.commit()
            return redirect(url_for('see_movies'))
        except:
            return 'There was an issue updating your movie'
    else:
        return render_template('update.html', movie=movie)
