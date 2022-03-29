'''Leadeboard Views'''
import itertools
import django_tables2 as tables
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib import messages
from movieguessr.models import Game, UserGame, Movie


td_center = {"td": {"align": "center"}, "th" : {"class": "text-center text-white-50"}}

class LeaderboardTable(tables.Table):
    '''LeaderboardTable'''
    counter = tables.Column(attrs=td_center, verbose_name="#", empty_values=(), orderable=False)
    user = tables.Column(attrs=td_center, orderable=False)
    total_score = tables.Column(attrs=td_center, orderable=False)

    def render_counter(self):
        # pylint: disable=attribute-defined-outside-init
        '''Rank'''
        self.row_counter = getattr(self, 'row_counter', itertools.count(1))
        return next(self.row_counter)

    class Meta:
        '''Meta'''
        row_attrs = {"style": "background-color: #D3D3D3"}
        template_name = "django_tables2/bootstrap.html"

class LeaderboardSpecificTable(tables.Table):
    '''LeaderboardSpecificTable'''
    counter = tables.Column(attrs=td_center, verbose_name="#", empty_values=(), orderable=False)
    user = tables.Column(attrs=td_center, orderable=False)
    tries = tables.Column(attrs=td_center, orderable=False)
    score = tables.Column(attrs=td_center, orderable=False)
    total_score = tables.Column(attrs=td_center, orderable=False)

    def render_counter(self):
        # pylint: disable=attribute-defined-outside-init
        '''Rank'''
        self.row_counter = getattr(self, 'row_counter', itertools.count(1))
        return next(self.row_counter)

    class Meta:
        '''Meta'''
        row_attrs = {"style": "background-color: #D3D3D3;"}
        template_name = "django_tables2/bootstrap.html"

def leaderboard(request):
    '''Shows the leaderboard'''
    if not request.user.is_authenticated:
        return HttpResponse("Unauthenticated")

    # Get all the users
    users = User.objects.all()
    for user in users:
        user.user = user.username
        user.total_score = total_score(user)

    # Sort the leaderboard
    users_sorted = sorted(list(users), key=lambda x: x.total_score, reverse=True)
    users_sorted = filter(lambda x: x.total_score != 0, users_sorted)

    scoretable = LeaderboardTable(users_sorted)

    return render(request, "leaderboard/main.html", {"scores":scoretable})

def search_movie_scores(request):
    '''Searches and shows specific Leaderboard'''
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

    scores = filter(lambda x: x.total_score != 0 and x.score != 0, scores)

    table = LeaderboardSpecificTable(scores)
    return render(request, "leaderboard/specific.html", {'movie' : movie_db, 'table' : table})

def total_score(user):
    '''Calulate total game score of a user.'''
    # Get all the user's games.
    games = UserGame.objects.filter(user_id=user.id)
    if not games:
        return 0

    return games.aggregate(Sum('score'))['score__sum']
