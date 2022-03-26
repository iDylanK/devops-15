from django.contrib import admin
from .models.game import Game
from .models.movie import Movie
from .models.user_game import UserGame


admin.site.register(Game)
admin.site.register(Movie)
admin.site.register(UserGame)