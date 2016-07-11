from django.http import HttpResponse
from django.shortcuts import render




def login(request):
    return HttpResponse("Login")


def register(request):
    return HttpResponse("Register")


def logout(request):
    return HttpResponse("Logout")


def ranking(request):
    return HttpResponse("User Ranking")


def profile(request, username):
    return HttpResponse("Profile Page of user: %s" % username)


def dashboard(request, username):
    return HttpResponse("Dashboard of user: %s" % username)


def edit_profile(request, username):
    return HttpResponse("Edit Profile of user: %s" % username)
