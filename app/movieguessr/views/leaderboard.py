from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from movieguessr.models import UserGame

def leaderboard(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthenticated")

    # Get all the users
    users = User.objects.all()
    for user in users:
        # Get all the user's games.
        games = UserGame.objects.filter(user_id=user.id)
        
        # Calculate total score
        total_score = 0
        for game in games:
            total_score += game.score
        user.total_score = total_score

    # Sort the leaderboard
    users_sorted = sorted(list(users), key=lambda x: x.total_score, reverse=True)

    return render(request, "leaderboard/main.html", {'users': users_sorted})