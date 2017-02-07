import math, random
from collections import Counter

from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .models import MACHOObject, Vote, PendingQuestion
from user.models import Expert


@login_required(login_url='/user/login/')
def hits_list(request):
    user = request.user
    expert = Expert.objects.get(user=request.user)
    num_voted = expert.vote_set.count()

    hits_query = PendingQuestion.objects.filter(expert=expert)
    hits_query = [hits.object for hits in hits_query]
    counter_hits = Counter(hits_query)
    hits_query = list(set(hits_query))

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

    hits_list = []
    for hits_instance in hits_query[start:end]:
        hits = dict()
        hits['hits_id'] = hits_instance
        hits['votes_left'] = counter_hits[hits_instance]
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

    hits_query = PendingQuestion.objects.filter(expert=expert)
    hits_query = [hits.object for hits in hits_query]
    next_id = random.choice(hits_query)
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
        print("POST")
        value = request.POST['value']
        question = request.POST['question']
        hits = MACHOObject.objects.get(pk=hits_id)
        expert = Expert.objects.get(user=request.user)
        question = PendingQuestion.objects.get(expert=expert, object=hits, question=question)

        try:
            if value.lower() == 'true':
                value = True
            else:
                value = False
            vote = Vote.objects.create(expert=expert, object=hits, 
                                        value=value, question=question.question)
            vote.save()
            question.delete()
            created = True
        except:
            created = False

        point = None
        if created:
            point = 1
            expert.update_level(point)

        #next_id = generate_next(expert)

        #json_response = {
        #    'point': point,
        #    'next': next_id
        #}
        #return JsonResponse(json_response)

    user = request.user
    expert = Expert.objects.get(user=user)
    hits = MACHOObject.objects.get(pk=hits_id)

    try:
    	question = PendingQuestion.objects.filter(expert=expert, object=hits)[0]
    except:
    	#next_id = generate_next(expert)
    	return hits_list(request)


    pre = ''
    if question.question in ['Eclipsing Binary']:
        pre = 'n'

    context = {
        'hits': hits,
        'user': user,
        'pre':pre,
        'question': question.question,
        'folded_image': "/static/media/images/"+str(hits.folded_image),
        'original_image': "/static/media/images/"+str(hits.original_image),
        'title': 'hits-detail',
    }
    return render(request, 'hits/hits-detail.html', context)


@login_required(login_url='/user/login/')
def hits_data(request, hits_id):
    hits = get_object_or_404(MACHOObject, pk=hits_id)
    hits_lightcurve = hits

    json_response = {
        'profile': "SHAKIRA",
    }
    return JsonResponse(json_response)


def learn(request):
    context = {
        'title': 'learn-hits',
    }
    return render(request, 'hits/hits-learn.html', context)
