'''Main Views'''

from django.shortcuts import render

def main(request):
    ''' Shows home / main page.'''
    return render(request, "main.html")
