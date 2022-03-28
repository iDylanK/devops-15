'''Auth Views'''

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as dlogout

def register(request):
    '''Register view'''
    if request.user.is_authenticated:
        return redirect("main")

    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Account created successfully')
            return redirect('main')

    else:
        user_form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': user_form})

def profile(request):
    '''Profile view'''
    return redirect('main')

def logout(request):
    '''Logout view'''
    dlogout(request)
    return redirect('main')
