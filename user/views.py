from django.http import HttpResponse, JsonResponse
from django.shortcuts import render




def login(request):
    return render(request, 'user/login.html')


def register(request):
    return render(request, 'user/register.html')


def logout(request):
    return HttpResponse("Logout")


def ranking(request):
    return render(request, 'user/ranking.html')


def ranking_data(request):
    pass


def profile(request, username):
    context = {
        'user': {
            'username': username
        }
    }
    return render(request, 'user/profile.html', context)

def edit_profile(request, username):
    context = {
        'user': {
            'username': username
        }
    }
    return render(request, 'user/editprofile.html', context)


def update_password(request, username):
    pass


def votes(request, username):
    pass


def activities(request, username):
    pass

def saved(request, username):
    pass
