import json

from django.contrib.auth.forms import (AuthenticationForm)

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .forms import UserCreateForm
from .models import Expert



def login_user(request):
    if request.user.is_authenticated():
        return redirect('main:index')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('main:index')

    login_form = AuthenticationForm()
    context = {
        'login_form': login_form
    }
    return render(request, 'user/login.html', context)


def register(request):

    if request.user.is_authenticated():
        return redirect('main:index')

    if request.method == "POST":
        user_form = UserCreateForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            # user.set_password(user.password)
            Expert.objects.create(user=user)
            user = authenticate(username=user.username, password=user.password)
            if user:
                print("here!")
                login(request, user)

            path = reverse('user:profile', kwargs={'username': user.username})
            return redirect(path)

    registeration_form = UserCreateForm()
    context = {
        'registeration_form': registeration_form,
    }
    return render(request, 'user/register.html', context)


@login_required(login_url='/user/login/')
def logout_user(request):
    logout(request)
    return redirect('main:index', permanent=True)


@login_required(login_url='/user/login/')
def ranking(request):
    with open('user/pseudouser.json', 'r') as f_data:
        pseudouser = json.load(f_data)
        pseudouser = pseudouser[0]
    pseudouser['is_authenticated'] = True
    period = request.GET['period']
    page = request.GET['page']
    user_per_page = 20

    ranking = []
    if period == 'A':
        with open('user/pseudousers.json','r') as pseudousers:
            pseudousers = json.load(pseudousers)
        for id, user in pseudousers.items():
            ranking.append(user)
        ranking = sorted(ranking, key=lambda x: -x['points'])
    else:
        pass

    context = {
        'user': pseudouser,
        'title': 'ranking',
        'period': period,
        'page': page,
        'ranking': ranking,
    }
    return render(request, 'user/ranking.html', context)


@login_required(login_url='/user/login/')
def profile(request, username):
    with open('user/pseudouser.json', 'r') as f_data:
        pseudouser = json.load(f_data)
        pseudouser = pseudouser[0]
    pseudouser['is_authenticated'] = True
    pseudouser['progress_hits'] = {
        'max': 2674,
        'num_voted': len(pseudouser['votehits']),
        'percent_complete': len(pseudouser['votehits'])/2674 * 100
    }
    # pseudouser['email'] = 'seongjung84@hotmail.com'
    pseudouser['activities'] = pseudouser['activities'][:25]
    context = {
        'user': pseudouser,
        'title': 'profile'
    }
    return render(request, 'user/profile.html', context)


def votes(request, username):
    pass


# def edit_profile(request, username):
#     pass
#
# def update_password(request, username):
#     pass
#
#
#
#
#
# def activities(request, username):
#     pass
#
# def saved(request, username):
#     pass
