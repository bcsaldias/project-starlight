from django.http import HttpResponse

from django.template import RequestContext
from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse


def index(request):
    #if request.user.is_authenticated():
    #    path = reverse('user:profile', kwargs={'username': request.user.username})
    #    return redirect(path)

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

def gratitude(request):
    context = {
        'title': 'learn'
    }
    return render(request, 'main/gratitude.html', context)



# HTTP Error 400
def my_page_not_found(request):
    response = render_to_response(
        '404.html',
        context_instance=RequestContext(request)
    )
    response.status_code = 400
    return response
