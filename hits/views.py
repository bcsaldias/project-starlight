import math, random

from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .models import MACHOObject, Vote
from user.models import Expert


@login_required(login_url='/user/login/')
def hits_list(request):
    user = request.user
    expert = Expert.objects.get(user=request.user)
    num_voted = expert.vote_set.count()

    hits_query = MACHOObject.objects.all()
    max_count = len(hits_query)

    percent_complete = 0
    if max_count > 0:
        percent_complete = num_voted / max_count * 100

    progress_hits = {
        'max': max_count,
        'num_voted': num_voted,
        'percent_complete': percent_complete
    }

    try:
        page = int(request.GET['page'])
    except:
        page = 1

    per_page = 20
    start = (page - 1) * per_page
    end = start+per_page
    max_page = math.ceil(max_count / 20)

    prev_pg=None
    if page > 1:
        prev_pg = page - 1
    next_pg=None
    if page < max_page:
        next_pg = page + 1

    pages = list(range(1,6,1))
    if page > 4:
        pages = [page+i for i in range(-2,3,1) if 0 < page+i <= max_page]

    hits_list = list()
    for hits_instance in hits_query[start:end]:
        hits = dict()
        hits['hits_id'] = hits_instance.pk
        #hits['periodLS'] = hits_instance.periodLS
        #hits['mag_mean'] = hits_instance.mag_mean
        try:
            vote = hits_instance.votes.get(expert=expert)
        except:
            hits['label'] = None
        else:
            hits['label'] = vote.label
        hits_list.append(hits)

    context = {
        'hits_list': hits_list,
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


def generate_next(expert):
    voted = set(expert.vote_set.values_list('object', flat=True))
    #expert, expert_id, id, object, object_id, question, value
    non_voted = list(MACHOObject.objects.values_list('pk',flat=True))
    non_voted = [hits_id for hits_id in non_voted if hits_id not in voted]

    next_id = random.choice(non_voted)

    return next_id


@login_required(login_url='/user/login/')
def hits_random(request):
    expert = get_object_or_404(Expert, user=request.user)

    next_id = generate_next(expert)

    path = reverse('hits:detail', args={next_id})
    return redirect(path)



@csrf_exempt
@login_required(login_url='/user/login/')
def hits_detail(request, hits_id):
    if request.method == "POST":
        label = request.POST['label']
        hits = MACHOObject.objects.get(pk=hits_id)
        expert = Expert.objects.get(user=request.user)

        try:
            vote = Vote.objects.get(expert=expert, hits=hits)
            created = False
        except Vote.DoesNotExist:
            vote = Vote.objects.create(expert=expert,
            hits=hits)
            created = True
        vote.label = label
        vote.save()

        point = None
        if created:
            point = 1
            expert.update_level(point)

        next_id = generate_next(expert)

        json_response = {
            'point': point,
            'next': next_id
        }
        return JsonResponse(json_response)

    user = request.user
    expert = Expert.objects.get(user=user)
    hits = get_object_or_404(MACHOObject, pk=hits_id)
    try:
        vote = hits.votes.get(expert=expert)
    except Vote.DoesNotExist:
        label = None
    else:
        label = vote.label
    context = {
        'hits': hits,
        'user': user,
        #'choices': Vote.HITS_LABELS,
        'label': label,
        'title': 'hits-detail'
    }
    return render(request, 'hits/hits-detail.html', context)


@login_required(login_url='/user/login/')
def hits_data(request, hits_id):
    hits = get_object_or_404(MACHOObject, pk=hits_id)
    hits_lightcurve = hits.hitsdetail_set.all()

    hits = serializers.serialize('json', [hits,])
    hits_lightcurve = serializers.serialize('json', hits_lightcurve, fields=('mjd','mag','err'))

    json_response = {
        'profile': hits,
        'lightcurve': hits_lightcurve
    }
    return JsonResponse(json_response)


def learn(request):
    context = {
        'title': 'learn-hits',
    }
    return render(request, 'hits/hits-learn.html', context)
