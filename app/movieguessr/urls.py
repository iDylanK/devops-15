"""movieguessr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import redirect

# Introduces security issues! But otherwise endpoints return 403s. Simple, bad solution for now
from django.views.decorators.csrf import csrf_exempt

import json

from datetime import datetime

# This should probably be called in another file, should be refactored.
from movieguessr.models import Movies, GamesOfTheDay, UserGames

@csrf_exempt
def create_account(request):
    body = json.loads(request.body)
    username = body['username']
    password = body['password']
    user = User.objects.filter(username=username)
    if user.exists():
        return error(request) # Maybe we can redirect instead?
    else:
        user = User.objects.create_user(username=username, password=password)
        user.save()
        # Redirect to game page? or maybe to login? Not sure how to do that.
        return login_endpoint(request)
        # return redirect("/login/")
        # return redirect("/")

@csrf_exempt
def login_endpoint(request):
    body = json.loads(request.body)
    username = body['username']
    password = body['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("/")

        # redirect to overview page?
        # return redirect
    else:
        return error(request)

# What is going to be on the home page? account creation?
@csrf_exempt
def main(request):
    return HttpResponse("Main")

@csrf_exempt
def game(request):
    userGame = find_game(request.user)
    if userGame is None:
        print("Help! No game today... Is a game missing in our database?")
        return redirect('/error/')
    
    if userGame.score > 0: # Meaning the game has already been played... What do we do? Redirect?
        return redirect("/gamewon/")

    if userGame.tries > 5: # Meaning the game has already been played... What do we do? Redirect?
        return redirect("/gamelost/")

    return HttpResponse("Game is going, make a guess")

@csrf_exempt
def gameguess(request):
    userGame = find_game(request.user)

    # How to handle duplication of this if statement? Making a function does not work as we need a return. Exception?
    if userGame is None:
        print("Help! No game today... Is a game missing in our database?")
        return redirect('/error/')

    if userGame.score > 0: # Meaning the game has already been played... What do we do? Redirect?
        return redirect("/gamewon/")

    if userGame.tries > 5: # Meaning the game has already been played... What do we do? Redirect?
        return redirect("/gamelost/")


    # We have loaded the game twice, theoretically could be next day now.
    dateTodayAsString = datetime.today().strftime('%Y-%m-%d')
    gameToday = GamesOfTheDay.objects.filter(date=dateTodayAsString).first()
    body = json.loads(request.body)
    guess = body['guess']
    if guess.lower() == gameToday.movie.title.lower():
        userGame.score = 1
        userGame.save(update_fields=['score'])
        return redirect("/gamewon/")
    else: 
        userGame.tries = userGame.tries + 1
        userGame.save(update_fields=['tries'])
        if userGame.tries > 5:
            return redirect("/gamelost/")

    return HttpResponse("Hmm... That doesn't seem right. Try again!")

@csrf_exempt
def gamewon(request):
    return HttpResponse("Game won! Please wait until tomorrow for the next game.")

@csrf_exempt
def gamelost(request):
    return HttpResponse("Game lost... Please wait until tomorrow for the next game.")

@csrf_exempt
def error(request):
    return HttpResponse("Error")

def find_game(user_id):
    dateTodayAsString = datetime.today().strftime('%Y-%m-%d')
    gameToday = GamesOfTheDay.objects.filter(date=dateTodayAsString).first()
    if gameToday is None:
        return None
    else:
        userGame = UserGames.objects.filter(user=user_id, game=gameToday.id).first()

    if userGame is None:
        userGame = UserGames(user=user_id, game=gameToday)
        userGame.save()
    # else: Well, it already exists, nothing to do...

    return userGame

urlpatterns = [
    path('create_account/', create_account),
    path('login/', login_endpoint),
    path('admin/', admin.site.urls),
    path('', main), 
    path('game/', game), # Game home page: Decide how this works with accounts.
    path('gameguess/', gameguess),
    path('gamewon/', gamewon),
    path('gamelost/', gamelost),
    path('error/', error)
]
