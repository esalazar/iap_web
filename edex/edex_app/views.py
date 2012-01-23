from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import Context, loader, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

from edex_app.models import Keyword
from edex_app.models import Profile
from edex_app.models import Institution
from edex_app.models import Course
from edex_app.models import Lecture
from edex_app.models import Note
from edex_app.models import Question
from edex_app.models import Answer

def index(request):
    context = {}
    context.update(csrf(request))
    context['index'] = True
    if request.user.is_authenticated():
        pass
    else:
        if request.method == 'POST':
            if 'login' == request.POST['type']:
                if not auth(request):
                    context['auth_error'] = "Incorrect username or password."
    return render_to_response('index.html', context, context_instance=RequestContext(request))

def institution(request, institution):
    context = {}
    context.update(csrf(request))
    if request.user.is_authenticated():
        pass
    else:
        if request.method == 'POST':
            if 'login' == request.POST['type']:
                if not auth(request):
                    context['auth_error'] = "Incorrect username or password."
    return render_to_response('institution.html', context, context_instance=RequestContext(request))

def course(request, institution, course):
    context = {}
    context.update(csrf(request))
    if request.user.is_authenticated():
        pass
    else:
        if request.method == 'POST':
            if 'login' == request.POST['type']:
                if not auth(request):
                    context['auth_error'] = "Incorrect username or password."
    return render_to_response('course.html', context, context_instance=RequestContext(request))

def lecture(request, institution, course, lecture):
    context = {}
    context.update(csrf(request))
    if request.user.is_authenticated():
        pass
    else:
        if request.method == 'POST':
            if 'login' == request.POST['type']:
                if not auth(request):
                    context['auth_error'] = "Incorrect username or password."
    return render_to_response('lecture.html', context, context_instance=RequestContext(request))

def search(request):
    context = {}
    context.update(csrf(request))
    if request.user.is_authenticated():
        pass
    else:
        if request.method == 'POST':
            if 'login' == request.POST['type']:
                if not auth(request):
                    context['auth_error'] = "Incorrect username or password."
    return render_to_response('search.html', context, context_instance=RequestContext(request))

def notes(request):
    context = {}
    context.update(csrf(request))
    if request.user.is_authenticated():
        pass
    else:
        if request.method == 'POST':
            if 'login' == request.POST['type']:
                if not auth(request):
                    context['auth_error'] = "Incorrect username or password."
    return render_to_response('notes.html', context, context_instance=RequestContext(request))

@login_required
def profile(request):
    context = {}
    context.update(csrf(request))
    if request.user.is_authenticated():
        pass
    else:
        if request.method == 'POST':
            if 'login' == request.POST['type']:
                if not auth(request):
                    context['auth_error'] = "Incorrect username or password."
    return render_to_response('profile.html', context, context_instance=RequestContext(request))

def registration(request):
    context = {}
    context.update(csrf(request))
    if request.user.is_authenticated():
        pass
    else:
        if request.method == 'POST':
            if 'login' == request.POST['type']:
                if not auth(request):
                    context['auth_error'] = "Incorrect username or password."
                else:
                    return HttpResponseRedirect('/edex/')
    return render_to_response('registration.html', context, context_instance=RequestContext(request))

def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return True
    return False

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/edex/")
