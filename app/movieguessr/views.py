from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Movies, Results
import requests, json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# Create your views here.
@csrf_exempt
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def test(request):
    return render(request, 'movieGuessr.html')

#@csrf_exempt
#def game(request):
#    return render(request, 'game.html')

class GameView(LoginRequiredMixin, TemplateView):
    template_name = 'game.html'


def callAPI(key, movieID):
    query = 'https://api.themoviedb.org/3/movie/' + movieID + \
    '?api_key=' + key + '&language=en-US'
    response = requests.get(query)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return "Unsuccessful API call"

def retrieveMovieOfTheDay():
    # get the first row from the Movies table
    return  Movies.objects.first()


def calculateScore(totalTries, tries, scoreMultiplier):
    
    return (totalTries - tries) * scoreMultiplier

def calculateTotalScore(user_id, score):
    #retrieve last game from Results for the user
    #total = user.games_set.order_by('id')[0]
    previousTotalScore = Results.objects.filter(user=user_id).order_by('-game_date').first().total_score
    return previousTotalScore + score

def getCurrentUserScores(request):

    if request.method == 'GET':
        scores = Results.objects.first() #filter(user=request.user.id)
        return render(request, '/movieGuesser.html',{'scores': scores})

def saveResults(user, movie, tries, score, totalScore):

    game = Results(user_id=user.pk, movie=movie, 
                 tries=tries, score=score, total_score=totalScore)
    game.save()

def getSpecificMovieLeaderboard(movie):
    # 10 highest scores
    return Results.objects.filter(movie=movie).order_by('score')[0:10]

def getTotalScoreLeaderBoard():
    # 10 highest total scores
    date = str(datetime.today().strftime('%Y-%m-%d'))
    return Results.objects.filter(date=date).order_by('total_score')[0:10]

#key = '2ab86fd0ac4102faa031205130740aa6'
#movieID = '550'

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
    movie_id = 549 # to start from 550 (the id for Fight Club)
    while saved_movies < 10: # make API calls until we have stored 10 movies
        movie_id += 1
        data = callAPI(key, str(movie_id))
        # if call is successful check that it includes all required info
        if data != None:
            try:
                img_url = data['backdrop_path']
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

            # only store if we have all hints available
            if (img_url != None and genres != None and title != None 
                and tagline != None and release_date != None 
                and summary != None):
                movie = Movies(title=title, image_url=img_url, genres=genres,
                        release_date=release_date, actor=actor, tagline=tagline,
                        summary=summary)
                movie.save()
                saved_movies += 1