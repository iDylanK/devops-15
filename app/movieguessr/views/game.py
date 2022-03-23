from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
import json

# This should probably be called in another file, should be refactored.
from movieguessr.models import Movies, GamesOfTheDay, UserGames
    

def game(request):
    return render(request, "game/daily.html")

def game_render(request):
    userGame = find_game(1)
    if userGame is None:
        print("Help! No game today... Is a game missing in our database?")
        return redirect('main')
    
    if userGame.score > 0: # Meaning the game has already been played... What do we do? Redirect?
        return redirect("/gamewon/")

    if userGame.tries > 5: # Meaning the game has already been played... What do we do? Redirect?
        return redirect("/gamelost/")

    return render(request, "game/daily.html")

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

def gamewon(request):
    return HttpResponse("Game won! Please wait until tomorrow for the next game.")

def gamelost(request):
    return HttpResponse("Game lost... Please wait until tomorrow for the next game.")

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