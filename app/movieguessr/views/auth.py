from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as dlogout

# def register(request):
#     return render(request, 'registration/register.html')

def register(request):
    if request.user.is_authenticated:
        return redirect("main")

    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('main')

    else:
        f = UserCreationForm()

    return render(request, 'registration/register.html', {'form': f})

def profile(request):
    return redirect('main')

def logout(request):
    dlogout(request)
    return redirect('main')