from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

# This should probably be called in another file, should be refactored.
from movieguessr.models import Game, Movie, UserGame
    

def game(request):
    # TODO: auth check DRY code.. middleware?
    if request.user is None:
        return HttpResponse("Unauthenticated")

    # TODO: game check DRY code.. middleware?
    user_game = find_game(request.user)
    if user_game is None:
        return HttpResponse("No game error..")
    
    daily_game = user_game.game
    guesses = user_game.tries
    
    # Check if the game is already played.
    if game_played(request, user_game):
        return redirect("main")

    return render(request, "game/daily.html", {'daily_game': daily_game, 'guesses': guesses, 'remaining': 6-guesses})

def game_guess(request):
    # TODO: auth check DRY code.. middleware?
    if request.user is None:
        return HttpResponse("Unauthenticated")

    # TODO: game check DRY code.. middleware?
    user_game = find_game(request.user)
    if user_game is None:
        return HttpResponse("No game error..")

    daily_game = user_game.game

    # Check if the game is already played.
    if game_played(request, user_game):
        return redirect("main")

    guess = request.POST.get('guess', '')
    if guess.lower().replace(" ", "") == daily_game.movie.title.lower().replace(" ", ""):
        user_game.score = user_game.tries + 1
        user_game.save(update_fields=['score'])
        return redirect("game_won")
    else: 
        user_game.tries = user_game.tries + 1
        user_game.save(update_fields=['tries'])
        if user_game.tries > 5:
            return redirect("game_lost")

    return redirect("game")

def game_won(request):
    if request.user is None:
        return HttpResponse("Unauthenticated")

    # TODO: game check DRY code.. middleware?
    user_game = find_game(request.user)
    if user_game is None:
        return HttpResponse("No game error..")

    if user_game.score == 0:
        return HttpResponse("Game error..")
    
    messages.add_message(request, messages.INFO, f'Game won with score: {user_game.score} !') 
    return redirect("main")

def game_lost(request):
    if request.user is None:
        return HttpResponse("Unauthenticated")

    # TODO: game check DRY code.. middleware?
    user_game = find_game(request.user)
    if user_game is None:
        return HttpResponse("No game error..")

    if user_game.tries < 6:
        return HttpResponse("Game error..")
    
    messages.add_message(request, messages.INFO, 'Game Lost!')
    return redirect("main")

def games_delete(request):
    if request.user is None:
        return HttpResponse("Unauthenticated")

    UserGame.objects.all().delete()
    return redirect("main")

def find_game(user_id):
    dateTodayAsString = datetime.today().strftime('%Y-%m-%d')
    # TODO: today game..
    # gameToday = Game.objects.filter(date=dateTodayAsString).first()
    daily_game = Game.objects.first()
    if daily_game is None:
        return None
    else:
        user_game = UserGame.objects.filter(user=user_id, game=daily_game.id).first()

    if user_game is None:
        user_game = UserGame(user=user_id, game=daily_game)
        user_game.save()
    # else: Well, it already exists, nothing to do...

    return user_game

def game_played(request, user_game):
    if user_game.score > 0: # Meaning the game has already been played... What do we do? Redirect?
        messages.add_message(request, messages.INFO, f'Game already played. Won with score: {user_game.score}')
        return True

    if user_game.tries > 5: # Meaning the game has already been played... What do we do? Redirect?
        messages.add_message(request, messages.INFO, 'Game already played. Lost')
        return True
    
    return False