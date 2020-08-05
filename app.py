#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2020 Jose Gonzalez ~ All rights reserved.

'''
Date: 4-8-2020
Description: Website about film catalog, uses json files as database
Deploy: Heroku app
'''

from flask import Flask, render_template, url_for, request
import json


class JSON():  # jsgonzlez661: Class for manager files json

    @classmethod
    def movies(cls):  # jsgonzlez661: Load file movies.json
        with open('static\\json\\movies.json') as file_json:
            movies = json.load(file_json)
            return movies

    @classmethod
    def genres(cls):  # jsgonzlez661: Load file genres.json
        with open('static\\json\\genres.json') as file_json:
            genres = json.load(file_json)
            return genres

    @classmethod
    def actors(cls):  # jsgonzlez661: Load file actors.json
        with open('static\\json\\actors.json') as file_json:
            actors = json.load(file_json)
            return actors

    @classmethod
    def directors(cls):  # jsgonzlez661: Load file directors.json
        with open('static\\json\\directors.json') as file_json:
            directors = json.load(file_json)
            return directors

    @classmethod
    def find_movie(cls, id):  # jsgonzlez661: Find movie for id
        movies = JSON.movies()
        for m in movies['movies']:
            if(m['id'] == id):
                return m

    @classmethod
    def find_movie_name(cls, name):  # jsgonzlez661: Find movie for title
        movies = JSON.movies()
        for m in movies['movies']:
            if(m['title'] == name):
                return m

    @classmethod
    def find_movie_gener(cls, name):  # jsgonzlez661: Find movie for geners
        genres = JSON.genres()
        movie_genre = []
        for g in genres['genres']:
            if(g['genrename'] == name):
                movie_genre.append(g['id'])
        return movie_genre

    @classmethod
    def find_genre(cls, id):  # jsgonzlez661: Find movie for actor
        genres = JSON.genres()
        movie_genre = []
        for g in genres['genres']:
            if(g['id'] == id):
                movie_genre.append(g)
        return movie_genre

    @classmethod
    def find_actor(cls, id):  # jsgonzlez661: Find movie for actor
        actors = JSON.actors()
        movie_actors = []
        for a in actors['actors']:
            if(a['id'] == id):
                movie_actors.append(a)
        return movie_actors

    @classmethod
    def find_director(cls, id):  # jsgonzlez661: Find movie for director
        directors = JSON.directors()
        movie_director = []
        for d in directors['directors']:
            if(d['id'] == id):
                movie_director.append(d)
        return movie_director

    @classmethod
    def filter_geners(cls):  # jsgonzlez661: Filter movie for geners
        genres = JSON.genres()
        geners = []
        for g in genres['genres']:
            if(g['genrename'] not in geners):
                geners.append(g['genrename'])
        geners = sorted(geners)
        return geners

    @classmethod
    def search_movies(cls, q):  # jsgonzlez661: Search movie for title
        movies = JSON.movies()
        movies_search = []
        for m in movies['movies']:
            if q in m['title']:
                movies_search.append(m)
            if q.upper() in m['title']:
                movies_search.append(m)
            if q.lower() in m['title']:
                movies_search.append(m)
            if q.capitalize() in m['title']:
                movies_search.append(m)

        search_movie = []
        for m in movies_search:
            if(m not in search_movie):
                search_movie.append(m)
        return search_movie


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
