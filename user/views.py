
import json

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .forms import UserCreateForm
from .models import Expert

from hits.models import MACHOObject


def login_user(request):
    if request.user.is_authenticated():
        path = reverse('user:profile', kwargs={'username': request.user.username})
        return redirect(path)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            redirect_path = reverse('user:profile', kwargs={'username': user.username})
            return redirect(redirect_path)

    return render(request, 'user/login.html')


def register(request):
    if request.user.is_authenticated():
        path = reverse('user:profile', kwargs={'username': request.user.username})
        return redirect(path)

    if request.method == "POST":

        user_form =  UserCreateForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            password = request.POST['password1']

            Expert.objects.create(user=user)

            user = authenticate(username=user.username, password=password)

            if user.is_authenticated():
                login(request, user)

            redirect_path = reverse('user:profile', kwargs={'username': user.username})
            return redirect(redirect_path)


    return render(request, 'user/register.html')


@login_required(login_url='/user/login/')
def logout_user(request):
    logout(request)
    return redirect('main:index')


@login_required(login_url='/user/login/')
def ranking(request):
    ranking = Expert.objects.order_by('-points')
    context = {
        'title': 'ranking',
        'ranking': ranking,
    }
    return render(request, 'user/ranking.html', context)


@login_required(login_url='/user/login/')
def profile(request, username):
    user = get_object_or_404(User, username=username)
    expert = Expert.objects.get(user=user)

    num_voted = expert.vote_set.count()
    max_count = MACHOObject.objects.count()

    percent_complete = 0
    if max_count > 0:
        percent_complete = num_voted / max_count * 100
        
    progress_hits = {
        'max': max_count,
        'num_voted': num_voted,
        'percent_complete': percent_complete
    }
    context = {
        'user': user,
        'progress_hits': progress_hits,
        'title': 'profile',
    }
    return render(request, 'user/profile.html', context)





# def votes(request, username):
#     pass
#
#
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
