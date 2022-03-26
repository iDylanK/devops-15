from django.shortcuts import render, redirect
from ..models.user_game import UserGame
from django.db.models import Sum
from django.http import HttpResponse
from ..models.game import Game
import django_tables2 as tables
from django.contrib.auth.models import User
from datetime import datetime


class SimpleTable(tables.Table):
    class Meta:
        model = UserGame
        row_attrs = {
            "style": "background-color: #D3D3D3;"
        }
        template_name = "django_tables2/bootstrap.html"

def leaderboard(request):

    if not request.user.is_authenticated:
        return HttpResponse("Unauthenticated")

    
    #total_score = UserGame.objects.filter(user=request.user.id).aggregate(Sum('score'))['score__sum']
    #return render(request, "leaderboard/main.html", {'total_score': total_score})

    users = User.objects.all()
    for user in users:
        # Get all the user's games.
        last_game = UserGame.objects.filter(user_id=user.id).order_by('-game__date').first()
        
        # Calculate total score
        total_score = last_game.total_score
        user.total_score = total_score

    # Sort the leaderboard
    users_sorted = sorted(list(users), key=lambda x: x.total_score, reverse=True)
    last_game = Game.objects.order_by('-id').first()
    scores = UserGame.objects.filter(game = last_game).order_by('-total_score')
    scoretable = SimpleTable(scores)
    return render(request, "leaderboard/main.html", {'scores': scoretable})


def searchMovieScores(request):
    
    if not request.user.is_authenticated:
        return HttpResponse("Unauthenticated")
    
    movie = request.POST.get('search', '')
    game_id  = Game.objects.get(movie__title=movie)
    scores = UserGame.objects.filter(game_id = game_id).order_by('-score')
    table = SimpleTable(scores)
    return render(request, "leaderboard/specific.html", {'movie' : movie, 'table' : table})
