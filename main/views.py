from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse


def index(request):
    if request.user.is_authenticated():
        path = reverse('user:profile', kwargs={'username': request.user.username})
        return redirect(path)

    return render(request, 'main/index.html')


def about(request):
    context = {
        'title': 'about'
    }
    return render(request, 'main/about.html', context)


def learn(request):
    context = {
        'title': 'learn'
    }
    return render(request, 'main/learn.html', context)
