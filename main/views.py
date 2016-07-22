from django.http import HttpResponse
from django.shortcuts import render



def index(request):
    # return HttpResponse("Index")
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def learn(request):
    return render(request, 'main/learn.html')
