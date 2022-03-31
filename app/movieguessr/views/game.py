'''Game Views'''

from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

# This should probably be called in another file, should be refactored.
from movieguessr.models import Game, UserGame

ALLOWED_TRIES = 6
SCORE_MULTIPLIER = 100

def game(request):
    '''Shows the main game page.'''
    # Check if authenticated
    if not request.user.is_authenticated:
        return HttpResponse("Unauthenticated")

    # Check for the game
    user_game = find_game(request.user)
    if user_game is None:
        messages.add_message(request, messages.INFO, 'No games today..')
        return redirect("main")

    daily_game = user_game.game
    guesses = user_game.tries

    # Check if the game is already played.
    if game_played(request, user_game):
        return redirect("main")

    return render(request, "game/daily.html", {'daily_game': daily_game, 'guesses': guesses, 'remaining': 6-guesses})

def game_guess(request):
    '''Makes a POST guess.'''
    # Check if authenticated
    if not request.user.is_authenticated:
        return HttpResponse("Unauthenticated")

    # Check for the game
    user_game = find_game(request.user)
    if user_game is None:
        return HttpResponse("No game error..")

    daily_game = user_game.game

    # Check if the game is already played.
    if game_played(request, user_game):
        return redirect("main")

    user_game.tries = user_game.tries + 1
    user_game.save(update_fields=['tries'])

    guess = request.POST.get('guess', '')
    if "".join(guess.lower().split()) == "".join(daily_game.movie.title.lower().split()):
        user_game.score = (ALLOWED_TRIES - user_game.tries + 1) * SCORE_MULTIPLIER
        user_game.save(update_fields=['score'])
        return redirect("game_won")

    if user_game.tries > 5:
        return redirect("game_lost")

    return redirect("game")

def game_won(request):
    '''Show the game won page.'''
    if not request.user.is_authenticated:
        return HttpResponse("Unauthenticated")

    user_game = find_game(request.user)
    if user_game is None:
        return HttpResponse("No game error..")

    if user_game.score == 0:
        return HttpResponse("Game error..")

    if user_game.tries == 1:
        messages.add_message(request, messages.INFO, f'Congratulations! \
            You guessed the movie in {user_game.tries} try. Score: {user_game.score}.')
    else:
        messages.add_message(request, messages.INFO, f'Congratulations! \
            You guessed the movie in {user_game.tries} tries. Score: {user_game.score}.')
    return redirect("main")

def game_lost(request):
    '''Show the game lost page.'''
    if not request.user.is_authenticated:
        return HttpResponse("Unauthenticated")

    user_game = find_game(request.user)
    if user_game is None:
        return HttpResponse("No game error..")

    if user_game.tries < 6:
        return HttpResponse("Game error..")

    messages.add_message(request, messages.INFO, f'You have used all {ALLOWED_TRIES} guesses unsuccessfully. \
        Better luck tomorrow! Movie Title: {user_game.game.movie}. Score: {user_game.score}.')
    return redirect("main")

def games_delete(request):
    '''Deletes all games from the database. For testing only..'''
    if not request.user.is_authenticated:
        return HttpResponse("Unauthenticated")

    UserGame.objects.all().delete()
    return redirect("main")

def find_game(user_id):
    '''Find a game'''
    try:
        daily_game = Game.objects.get(movie__title = "The Ring")#date=datetime.today().strftime('%Y-%m-%d'))
    except:
        return None

    user_game = UserGame.objects.filter(user=user_id, game=daily_game.id).first()
    if user_game is None:
        user_game = UserGame(user=user_id, game=daily_game)
        user_game.save()
    # else: Well, it already exists, nothing to do...

    return user_game

def game_played(request, user_game):
    '''Check if a game is played by a user before.'''
    if user_game.score > 0: # Meaning the game has already been played... What do we do? Redirect?
        messages.add_message(request, messages.INFO, f'You have already played the day\'s game. \
            Movie Title: {user_game.game.movie}. Your score: {user_game.score}. Come back tomorrow for a new movie!')
        return True

    if user_game.tries > 5: # Meaning the game has already been played... What do we do? Redirect?
        messages.add_message(request, messages.INFO, f'You have already played the day\'s game. \
            Movie Title: {user_game.game.movie}. Your score: {user_game.score}. Come back tomorrow for a new movie!')
        return True

    return False
