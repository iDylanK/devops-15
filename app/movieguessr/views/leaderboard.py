from django.shortcuts import render, redirect

def leaderboard(request):
    return render(request, "leaderboard/main.html")