
import json
import numpy as np
#CHOICES = ['Cepheid','RR Lyrae', 'Long-period variable', 'Eclipsing Binary']
CHOICES = ['CEP','RRLYR','LPV','EB']

N_CHOICES = len(CHOICES)

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction

from .forms import UserCreateForm
from .models import Expert

from hits.models import CatalinaObject, PendingQuestion, FullPendingQuestion


from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext as _


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


@transaction.atomic
def register(request):
    
    if request.user.is_authenticated():
        path = reverse('user:profile', kwargs={'username': request.user.username})
        return redirect(path)

    if request.method == "POST":

        user_form =  UserCreateForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            password = request.POST['password1']

            expert = Expert.objects.create(user=user)
            expert.user.first_name = request.POST['first_name']
            expert.user.last_name = request.POST['last_name']
            expert.user.save()
            # Create the questions.
            objects_training = CatalinaObject.objects.filter(_training=True)
            objects_validation = CatalinaObject.objects.filter(_validation=True)
            objects_abc = CatalinaObject.objects.filter(_abc=True)

            _p_questions_yn = []
            _p_questions_abc = []


            for hits in objects_training:

                Nq=np.random.randint(1, N_CHOICES+1)
                ma=np.random.choice(CHOICES,Nq,replace=False)
                for label in ma:
                    p_question = PendingQuestion.objects.create(expert=expert, object=hits, nquestions = Nq)
                    p_question.question = label
                    _p_questions_yn.append(p_question)

                p_question = FullPendingQuestion.objects.create(expert=expert, object=hits)
                _p_questions_abc.append(p_question)

            for hits in objects_validation:
                Nq=np.random.randint(1, N_CHOICES+1)
                ma=np.random.choice(CHOICES,Nq,replace=False)
                for label in ma:
                    p_question = PendingQuestion.objects.create(expert=expert, object=hits, nquestions = Nq)
                    p_question.question = label
                    _p_questions_yn.append(p_question)
            
            for hits in objects_abc:
                p_question = FullPendingQuestion.objects.create(expert=expert, object=hits)
                _p_questions_abc.append(p_question)


            expert.initial_yn_questions = len(_p_questions_yn)
            expert.initial_abc_questions = len(_p_questions_abc)
            expert.save()

            np.random.shuffle(_p_questions_yn)
            np.random.shuffle(_p_questions_abc)
            for p_question in _p_questions_yn:
                p_question.save()
            for p_question in _p_questions_abc:
                p_question.save()

            del _p_questions_yn
            del _p_questions_abc

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
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('main:index')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {'form': form})

@login_required(login_url='/user/login/')
def change_name(request):
    if request.method == 'POST':
        try:
            print(request.user.first_name)
            request.user.first_name = request.POST['first_name']
            request.user.last_name = request.POST['last_name']
            request.user.save()
            path = reverse('user:profile', kwargs={'username': request.user.username})
            return redirect(path)            
        except:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_name.html', {'form': form})

@login_required(login_url='/user/login/')
def profile(request, username):
    user = get_object_or_404(User, username=username)

    try:
        expert = Expert.objects.get(user=user)
    except:
        logout(request)
        return render(request, 'user/login.html')


    num_voted_yn = expert.pendingquestion_set.count()
    num_voted_abc = expert.fullpendingquestion_set.count()

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
    context = {
        'user': user,
        'progress_hits': progress_hits,
        'title': 'profile',
        'original_user': request.user.username
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
