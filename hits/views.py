import json, math

from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Hits, HitsDetail
from user.models import Expert


def learn(request):
    pass

@login_required(login_url='/user/login/')
def hits_list(request):
    user = request.user
    expert = Expert.objects.get(user=request.user)
    num_voted = expert.votehits_set.count()

    hits_list = Hits.objects.all()
    max_count = len(hits_list)
    progress_hits = {
        'max': max_count,
        'num_voted': num_voted,
        'percent_complete': num_voted / max_count * 100
    }

    try:
        page = int(request.GET['page'])
    except:
        page = 1

    per_page = 20
    start = (page - 1) * per_page
    end = start+per_page
    max_page = math.ceil(len(hits_list) / 20)

    prev_pg=None
    if page > 1:
        prev_pg = page - 1
    next_pg=None
    if page < max_page:
        next_pg = page + 1

    pages = list(range(1,6,1))
    if page > 4:
        pages = [page+i for i in range(-2,3,1) if 0 < page+i <= max_page]

    context = {
        'hits_list': hits_list[start:end],
        'page': page,
        'next': next_pg,
        'prev': prev_pg,
        'pages': pages,
        'max_page': max_page,
        'user': user,
        'progress_hits': progress_hits,
        'title': 'hits-list'
    }
    return render(request, 'hits/hits-list.html', context)


@csrf_exempt
@login_required(login_url='/user/login/')
def hits_detail(request, hits_id):
    if request.method == "POST":
        json_response = {
            'point': 1,
            'next': 'Blind15A_04_N16_0183_3344'
        }
        return JsonResponse(json_response)

    user = request.user
    expert = Expert.objects.get(user=user)

    context = {
        'hits_id': hits_id,
        'user': user,
        'title': 'hits-detail'
    }
    return render(request, 'hits/hits-detail.html', context)


@login_required(login_url='/user/login/')
def hits_data(request, hits_id):
    hits = get_object_or_404(Hits, pk=hits_id)
    hits_lightcurve = hits.hitsdetail_set.all()

    hits = serializers.serialize('json', [hits,])
    hits_lightcurve = serializers.serialize('json', hits_lightcurve, fields=('mjd','mag','err'))

    json_response = {
        'profile': hits,
        'lightcurve': hits_lightcurve
    }
    return JsonResponse(json_response)


# def hits_save(request, hits_id):
#     pass
