from django.http import HttpResponse
from django.shortcuts import render




def login(request):
    return render(request, 'user/login.html')


def register(request):
    return render(request, 'user/register.html')


def logout(request):
    return HttpResponse("Logout")


def ranking(request):
    return render(request, 'user/ranking.html')


def profile(request, username):
    context = {
        'user': {
            'username': username
        }
    }
    return render(request, 'user/profile.html', context)


def dashboard(request, username):
    context = {
        'user': {
            'username': username
        }
    }
    return render(request, 'user/dashboard.html', context)


def edit_profile(request, username):
    context = {
        'user': {
            'username': username
        }
    }
    return render(request, 'user/editprofile.html', context)
