from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Mimetypes for images
from mimetypes import guess_type

# App Models
from app.models import *
from app.game_settings import *

# 
import os
import sys
import json

# Twill for CN login
from twill import commands

@login_required
def question(request):
    context = {
        'page': 'question'
    }

    userid = request.user.id
    user = get_object_or_404(Student, id= userid)
    context['user'] = user

    level = get_level(user)
    context['level'] = level
    context['question'] = create_question(user, user.college, level)

    return render(request, 'pages/question.html', context)

def about(request):
    context = {}
    return render(request, 'pages/about.html', context)

def highscore(request):
    context = {}
    return render(request, 'pages/highscore.html', context)

@login_required
def answer_question(request):
    user = get_object_or_404(Student, id =request.user)

    if request.method != 'POST':
        raise Http404

    if not 'uid' in request.POST or request.POST['uid'] or \
        not 'answer' in request.POST or request.POST['answer'] or \
        not 'q_type' in request.POST or request.POST['q_type']:
            raise Http404

    target = get_object_or_404(Student, id=request.POST['uid'])
    q_type = request.POST['q_type']
    correct = verify_question(user, target, q_type, request.POST['answer'])

    result = {}
    if correct:
        result['result'] = True

        old_level = get_level(user)
        added_points = dict(QUESTION_TYPES)[ q_type ]
        user.points += added_points
        user.save()
        col = College.objects.get(name=user.college)
        col.points += added_points
        col.save()
        new_level = get_level(user)

        result['new_points'] = added_points
        result['new_total'] = user.points
        result['new_total_college'] = col.points
        if old_level != new_level:
            result['levelup'] = True
    else:
        result['result'] = False

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def home(request):
    if request.user and request.user.is_authenticated():
        return redirect('/question')
    context = {
        'page': 'home'
    }
    if request.method == 'GET':
        return render(request, "pages/home.html", context)

    if request.method != 'POST':
        raise Http404

    if not 'user' in request.POST or not request.POST['user'] or \
        not 'pass' in request.POST or not request.POST['pass']:
            context['error'] = "The username does not exist in the DB!"
            return render(request, "pages/home.html", context)

    l_username = request.POST['user']
    # Uncomment this when testing is done
    # cn_page = campusnet_login(request.POST['user'], request.POST['pass'])

    # if cn_page.find('Wrong username or password') != -1:
    #     context['error'] = "Wrong username or password!"
    #     return render(request, "pages/login_page.html", context)
    
    users = Student.objects.filter(username=l_username)
    if len(users) != 1:
        context['error'] = "The username does not exist in the DB!"
        return render(request, "pages/home.html", context)

    user = authenticate(username=l_username, password="1234")
    if user is not None:
        if not user.is_active:
            user.active = True
            user.save()

        login(request, user)
        return redirect('/question')

    context['error'] = "Invalid login! Please try again!"
    return render(request, "pages/home.html", context)

@login_required
def logout_action(request):
    if request.user:
        user = request.user
    logout(request)
    return redirect('/')


def campusnet_login(l_username, l_password):
    commands.go('https://campusnet.jacobs-university.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=ACTION&ARGUMENTS=-A9PnS7.Eby4LCWWmmtOcbYKUQ-so-sF48wtHtVNWX9aIeYmoSh5mej--SCbT.jubdlAouHy3dHzwyr-O.ufj3NVAYCNiJr0CFcBNwA3xADclRCTyqC0Oip8drT0F=')
    commands.fv('1', 'usrname', l_username)
    commands.fv('1', 'pass', l_password)
    commands.submit('3')

    out = sys.stdout
    bin = open(os.devnull, 'w')
    sys.stdout = bin
    returned_page = commands.show()
    sys.stdout = out

    return returned_page
