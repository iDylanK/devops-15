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
from django.urls import path
from django.conf.urls import include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.main, name='main'),

    path('accounts/logout/', views.logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.profile),
    path('accounts/games/delete/', views.games_delete, name="games_delete"), # Testing only..
    path('accounts/movies/add/', views.add_movies, name="add_movies"),

    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('leaderboard/search', views.search_movie_scores, name='search'),

    path('game/', views.game, name='game'), # Game home page: Decide how this works with accounts.
    path('game/guess/', views.game_guess, name="guess"),
    path('game/won/', views.game_won, name="game_won"),
    path('game/lost/', views.game_lost, name="game_lost"),

    path('admin/', admin.site.urls),
]
