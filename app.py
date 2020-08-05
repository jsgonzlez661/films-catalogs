#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2020 Jose Gonzalez ~ All rights reserved. MIT license.

'''
Date: 4-8-2020
Description: Website about film catalog, uses json files as database
Deploy: Heroku app
'''

from flask import Flask, render_template, url_for, request
from json_app import JSON


app = Flask(__name__)


@app.route('/')  # jsgonzlez661: Route index page
def index():
    movies = JSON.movies()
    page = request.args.get('page', type=int, default=1)
    # jsgonzlez661: Paginate movies
    all_movies = [movies['movies'][i:i + 24]
                  for i in range(0, len(movies['movies']), 24)]
    return render_template('index.html', movies=all_movies[page - 1],
                           page=page, genres=JSON.filter_geners())


@app.route('/movie/<string:name>')  # jsgonzlez661: Route for information movie
def movie(name):
    movie = JSON.find_movie_name(name)
    id = movie['id']
    return render_template('movie.html', movie=movie,
                           genres=JSON.find_genre(id), actors=JSON.find_actor(id),
                           directors=JSON.find_director(id))


# jsgonzlez661: Route for filter geners movie
@app.route('/genre/<string:genre>')
def genere(genre):
    id_genre = JSON.find_movie_gener(genre)
    movies = JSON.movies()
    fullmovie = []
    for id in id_genre:
        for m in movies['movies']:
            if(m['id'] == id):
                fullmovie.append(m)
    return render_template('genre.html', movies=fullmovie, genres=JSON.filter_geners(), name=genre)


# jsgonzlez661: Route search movie for title
@app.route('/search', methods=['POST'])
def search():
    q = request.form['search']
    return render_template('search.html', movies=JSON.search_movies(q), genres=JSON.filter_geners(), name="Search")

if __name__ == '__main__':
    app.run()
