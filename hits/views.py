import math, random
from collections import Counter
import numpy as np

from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .models import CatalinaObject, Vote, PendingQuestion, FullVote, FullPendingQuestion
from user.models import Expert

_CHOICES = ['Cepheid','RR Lyrae', 'Long-period variable', 'Eclipsing Binary']
CHOICES = ['CEP','RRLYR','LPV','EB']
show_question = dict(zip(CHOICES, _CHOICES))

@login_required(login_url='/user/login/')
def hits_list(request):
    user = request.user
    expert = Expert.objects.get(user=request.user)
    
    num_voted_yn = expert.pendingquestion_set.count()
    num_voted_abc = expert.fullpendingquestion_set.count()

    hits_query = Vote.objects.filter(expert=expert)
    hits_query = [hits.object for hits in hits_query]
    hits_query += [hits.object for hits in FullVote.objects.filter(expert=expert)]

    counter_hits = Counter(hits_query)
    hits_query = list(set(hits_query))
    #hits_query = sorted(hits_query, key=lambda x: int(x.catalina_id))

    max_count = expert.initial_abc_questions + expert.initial_yn_questions

    percent_complete = 0
    if max_count > 0:
        percent_complete = (max_count-num_voted_yn-num_voted_abc) / max_count * 100

    num_voted = expert.vote_set.count() + expert.fullvote_set.count()

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
        hits['votes_given'] = counter_hits[hits_instance]
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


def generate_next(expert, hits=None):

    prob= random.random()
    if prob > .15:
        hits_query = PendingQuestion.objects.filter(expert=expert)[:20]
        if len(hits_query) > 0:
            hits_query = [hits.object.catalina_id for hits in hits_query]
            next_id = random.choice(hits_query)
            return next_id, 'yn'
    else:
        hits_query = FullPendingQuestion.objects.filter(expert=expert)[:20]
        if len(hits_query) > 0:
            next_id = random.choice(hits_query)
            return next_id.object_id, 'abc'
        else:
            hits_query = PendingQuestion.objects.filter(expert=expert)[:20]
            if len(hits_query) > 0:
                hits_query = [hits.object.catalina_id for hits in hits_query]
                next_id = random.choice(hits_query)
                return next_id, 'yn'
    return None, None


@login_required(login_url='/user/login/')
def hits_random(request):
    expert = get_object_or_404(Expert, user=request.user)

    next_id, question_type = generate_next(expert)
    path = reverse('hits:detail', args={next_id})

    return redirect(path)

def calculate_point(expert):
    _votes = Vote.objects.filter(expert=expert)
    _full_votes = FullVote.objects.filter(expert=expert)

    _votes = np.array([[vote.value, 
                        vote.question, 
                        vote.object.Var_Type] for vote in _votes])

    diag = 0
    rest = 0
    for vote in _votes:
        if vote[1] == vote[2]:
            if vote[0] == 'True':
                diag +=1
            else:
                rest += 1
        else:
            if vote[0] == 'False':
                diag +=1
            else:
                rest += 1
    _sum = diag
                
    _full_votes = np.array([[vote.value, 
                            vote.object.Var_Type] for vote in _full_votes])
    if len(_full_votes) > 0:
        _sum += (_full_votes[:,0] == _full_votes[:,1]).sum()

    return _sum / (diag+rest+len(_full_votes))


@csrf_exempt
@login_required(login_url='/user/login/')
def hits_detail(request, hits_id):
    if request.method == "POST": 
            
        value = request.POST['value']
        hits = CatalinaObject.objects.get(pk=hits_id)
        expert = Expert.objects.get(user=request.user)
        question_type = request.POST['question_type']
        milliseconds = request.POST['milliseconds']

        if question_type == 'yn':
            question = request.POST['private_question']
            question = PendingQuestion.objects.get(expert=expert, object=hits, question=question)

            try:
                if value.lower() == 'true':
                    value = True
                else:
                    value = False
                vote = Vote.objects.create(expert=expert, object=hits, 
                                            value=value, question=question.question, 
                                            milliseconds=milliseconds)
                vote.save()
                question.delete()
                created = True
            except:
                created = False

        elif question_type == 'abc':

            question = FullPendingQuestion.objects.get(expert=expert, object=hits)

            try:
                vote = FullVote.objects.create(expert=expert, object=hits, 
                                            value=value, milliseconds=milliseconds)
                vote.save()
                question.delete()
                created = True
            except:
                created = False


        next_id, question_type = generate_next(expert, hits)

        point = None
        if created:
            point = calculate_point(expert)
            expert.update_level(point)

        json_response = {
            'point': point,
            'next': next_id,
            'question_type': question_type
        }
        return JsonResponse(json_response)

    user = request.user
    expert = Expert.objects.get(user=user)
    hits = CatalinaObject.objects.get(pk=hits_id)

    try:
        question = PendingQuestion.objects.filter(expert=expert, object=hits)[0]
        pre = ''
        if question.question in ['EB']:
            pre = 'n'

        context = {
            'hits': hits,
            'user': user,
            'pre':pre,
            'private_question': question.question,
            'question': show_question[question.question],
            'folded_image': "/static/media/images/"+str(hits.folded_image),
            'original_image': "/static/media/images/"+str(hits.original_image),
            'title': 'hits-detail',
            'question_type': 'yn'
        }
        return render(request, 'hits/hits-detail.html', context)
    except:
        pass

    try:
        question = FullPendingQuestion.objects.filter(expert=expert, object=hits)[0]
        context = {
            'hits': hits,
            'user': user,
            'question':'',
            'folded_image': "/static/media/images/"+str(hits.folded_image),
            'original_image': "/static/media/images/"+str(hits.original_image),
            'title': 'hits-detail',
            'question_type': 'abc'
        }
        return render(request, 'hits/hits-detail.html', context)
    except:
        return hits_list(request)




@login_required(login_url='/user/login/')
def hits_data(request, hits_id):
    hits = get_object_or_404(CatalinaObject, pk=hits_id)
    hits_lightcurve = hits

    json_response = {
        'profile': "SHAKIRA",
    }
    return JsonResponse(json_response)


def learn(request):
    context = {
        'title': 'learn-catalina',
    }
    return render(request, 'hits/hits-learn.html', context)
