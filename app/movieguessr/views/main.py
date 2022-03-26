import requests
from django.http import HttpResponse
from django.contrib import messages
from ..models.movie import Movie
from ..models.game import Game
from django.shortcuts import render, redirect
from datetime import datetime, timedelta


def main(request):
    return render(request, "main.html")

def add_movies(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthenticated")
    
    movies = storeMovies()
    messages.add_message(request, messages.INFO, f'Movies added: {movies} .')
    return redirect("main")


def callAPI(key, movieID):
    query = 'https://api.themoviedb.org/3/movie/' + movieID + \
    '?api_key=' + key + '&append_to_response=credits'
    response = requests.get(query)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        #print("Unsuccessful API call: " + str(response.status_code))
        return None


def storeMovies():
    
    key = '2ab86fd0ac4102faa031205130740aa6'
    saved_movies = 0
    movie_list = []
    movie_id = 549 # to start from 550 (the id for Fight Club)
    while saved_movies < 5: # make API calls until we have stored 10 movies
        movie_id += 1
        data = callAPI(key, str(movie_id))
        # if call is successful check that it includes all required info
        if data != None:
            try:
                img_url = "https://image.tmdb.org/t/p/original" + data['backdrop_path']
            except:
                img_url = None
            try:
                genres = data['genres'][0]['name']
            except:
                genres = None
            try:
                title = data['title']
            except:
                title = None
            try:
                tagline = data['tagline']
            except:
                tagline = None
            try:
                release_date = data['release_date']
            except:
                release_date = None
            try:
                summary = data['overview']
            except:
                summary = None  
            try:
                actor = data['credits']['cast'][0]['name']
            except:
                actor = None
            try:
                character = data['credits']['cast'][0]['character']
            except:
                actor = None

            # only store if we have all hints available
            if (img_url != None and genres != None and title != None 
                and tagline != None and release_date != None 
                and summary != None):
                movie = Movie(title=title, image_url=img_url, genres=genres,
                        release_date=release_date, actor=actor, character=character, tagline=tagline,
                        summary=summary)
                try:
                    movie.save()
                    previous_date = Game.objects.last().date
                    if previous_date != None:
                        year = int(previous_date[:4])
                        month = int(previous_date[5:7])
                        day = int(previous_date[-2:])
                        next_date = datetime(year, month, day) + timedelta(days=1)
                        next_date_str = next_date.strftime('%Y-%m-%d')
                        print(next_date_str)
                    else:
                        next_date_str = datetime.today().strftime('%Y-%m-%d')
                    game = Game(date=next_date_str, movie=movie.pk)
                    game.save()
                    movie_list.append(movie.title)
                    saved_movies += 1
                except:
                    continue
    return movie_list