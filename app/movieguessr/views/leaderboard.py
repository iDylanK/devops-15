from django.shortcuts import render, redirect
from django.http import HttpResponse
from movieguessr.models import Game, UserGame, Movie
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib import messages

import django_tables2 as tables

td_center = {"td": {"align": "center"}}

class LeaderboardTable(tables.Table):
    user = tables.Column(attrs=td_center)
    total_score = tables.Column(attrs=td_center)
    
    class Meta:
        row_attrs = {
            "style": "background-color: #D3D3D3"
        }
        template_name = "django_tables2/bootstrap.html"

class LeaderboardSpecificTable(tables.Table):
    user = tables.Column(attrs=td_center)
    tries = tables.Column(attrs=td_center)
    score = tables.Column(attrs=td_center)
    total_score = tables.Column(attrs=td_center)
    
    class Meta:
        row_attrs = {
            "style": "background-color: #D3D3D3;"
        }
        template_name = "django_tables2/bootstrap.html"

def leaderboard(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthenticated")

    # Get all the users
    users = User.objects.all()
    for user in users:
        user.user = user.username
        user.total_score = total_score(user)

    # Sort the leaderboard
    users_sorted = sorted(list(users), key=lambda x: x.total_score, reverse=True)

    scoretable = LeaderboardTable(users_sorted)

    return render(request, "leaderboard/main.html", {"scores":scoretable})


def search_movie_scores(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthenticated")
    
    movie = request.POST.get('search', '')

    try:
        movie_db = Movie.objects.get(title=movie)
        game = Game.objects.get(movie_id=movie_db.id)
    except: 
        messages.add_message(request, messages.INFO, f'Movie {movie} not found.') 
        return redirect("leaderboard")
        
    scores = list(UserGame.objects.filter(game_id = game.id).order_by('-score'))

    for score in scores:
        # score.user = score.user
        score.total_score = total_score(score.user)

    table = LeaderboardSpecificTable(scores)
    return render(request, "leaderboard/specific.html", {'movie' : movie, 'table' : table})

def total_score(user):
     # Get all the user's games.
    games = UserGame.objects.filter(user_id=user.id)
    return games.aggregate(Sum('score'))['score__sum']