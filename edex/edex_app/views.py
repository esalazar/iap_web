from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import Context, loader, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

from django.contrib.auth.models import User

from edex_app.models import Keyword
from edex_app.models import Profile
from edex_app.models import Institution
from edex_app.models import Course
from edex_app.models import Lecture
from edex_app.models import Note
from edex_app.models import Question
from edex_app.models import Answer

import conf

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
                    context['auth_error'] = 'Incorrect username or password.'
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
                    context['auth_error'] = 'Incorrect username or password.'
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
                    context['auth_error'] = 'Incorrect username or password.'
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
                    context['auth_error'] = 'Incorrect username or password.'
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
                    context['auth_error'] = 'Incorrect username or password.'
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
                    context['auth_error'] = 'Incorrect username or password.'
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
                    context['auth_error'] = 'Incorrect username or password.'
    return render_to_response('profile.html', context, context_instance=RequestContext(request))

def registration(request):
    context = {}
    context.update(csrf(request))
    context['languages'] = conf.LANGUAGES
    if request.user.is_authenticated():
        return HttpResponseRedirect("/edex/")
    else:
        if request.method == 'POST':
            if 'login' == request.POST['type']:
                if not auth(request):
                    context['auth_error'] = 'Incorrect username or password.'
                else:
                    return HttpResponseRedirect('/edex/')
            elif 'registration' == request.POST['type']:
                username = request.POST['username']
                first_name = request.POST['firstname']
                last_name = request.POST['lastname']
                email = request.POST['email']
                password = request.POST['password']
                repassword = request.POST['repassword']
                language = request.POST['language']
                if User.objects.filter(username=username).exists():
                    context['registration_error'] = 'Error: Username cannot be used.'
                elif User.objects.filter(email=email).exists():
                    context['registration_error'] = 'Error: Email cannot be used.'
                elif password != repassword:
                    context['registration_error'] = 'Error: Mismatching passwords.'
                elif password == '':
                    context['registration_error'] = 'Error: No empty passwords.'
                elif language == '':
                    context['registration_error'] = 'Error: Please choose a language.'
                elif first_name == '':
                    context['registration_error'] = 'Error: Please enter a first name.'
                elif last_name == '':
                    context['registration_error'] = 'Error: Please enter a last name.'
                else:
                    try:
                        user = User.objects.create_user(username=username, email=email, password=password)
                        user.first_name = first_name
                        user.last_name = last_name
                        user.save()
                        profile = Profile(user=user, language=language)
                        profile.save()
                        if not auth(request):
                            context['auth_error'] = 'Incorrect username or password.'
                        else:
                            return HttpResponseRedirect('/edex/')
                    except:
                        context['registration_error'] = 'Error with registration.'
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
