from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import Context, loader, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.contrib.auth.models import User
from edex_app.models import *
from haystack.query import SearchQuerySet, EmptySearchQuerySet

import conf

def index(request):
    context = {}
    context.update(csrf(request))
    context['auth_error'] = check_if_login(request)
    context['related_lectures'] = get_related_lectures(request)
    context['index'] = True
    context['keywords'] = Keyword.objects.order_by('?')[:10]
    return render_to_response('index.html', context, context_instance=RequestContext(request))

def institution(request, institution):
    context = {}
    context.update(csrf(request))
    context['auth_error'] = check_if_login(request)
    context['related_lectures'] = get_related_lectures(request)
    return render_to_response('institution.html', context, context_instance=RequestContext(request))

def course(request, course_pk):
    context = {}
    context.update(csrf(request))
    context['auth_error'] = check_if_login(request)
    context['related_lectures'] = get_related_lectures(request)
    try:
        context['course'] = Course.objects.get(pk=course_pk)
        context['lectures'] = get_lectures(context['course'])
    except:
        raise Http404('The course does not exist.')
    return render_to_response('course.html', context, context_instance=RequestContext(request))

def lecture(request, course_pk, lecture_num):
    context = {}
    context.update(csrf(request))
    context['auth_error'] = check_if_login(request)
    context['related_lectures'] = get_related_lectures(request)
    try:
        context['course'] = Course.objects.get(pk=course_pk)
        context['lectures'] = get_lectures(context['course'])
        context['lecture_num'] = int(lecture_num)
        context['lecture_video_id'] = Lecture.objects.filter(course=context['course'], number=lecture_num)[0].video
    except:
        raise Http404('The course does not exist.')
    return render_to_response('course.html', context, context_instance=RequestContext(request))

def search(request):
    context = {}
    context.update(csrf(request))
    context['auth_error'] = check_if_login(request)
    context['related_lectures'] = get_related_lectures(request)

    results_per_page = 10
    if request.GET.get('text'):
        course_results = EmptySearchQuerySet()
        text = request.GET['text']
        course_results = SearchQuerySet().filter(content=SearchQuerySet().query.clean(text)).models(Course)
        
        paginator = Paginator(course_results, results_per_page)
        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("No such page of results!")
        context['text'] = text
        context['page'] = page
        context['paginator'] = paginator
    return render_to_response('search.html', context, context_instance=RequestContext(request))

def notes(request):
    context = {}
    context.update(csrf(request))
    context['auth_error'] = check_if_login(request)
    context['related_lectures'] = get_related_lectures(request)
    return render_to_response('notes.html', context, context_instance=RequestContext(request))

def profile(request, username):
    context = {}
    context.update(csrf(request))
    context['auth_error'] = check_if_login(request)
    context['related_lectures'] = get_related_lectures(request)
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.filter(user=user)[0]
        context['user_profile'] = user_profile
    except:
        raise Http404('Cannot find that user.')
    return render_to_response('profile.html', context, context_instance=RequestContext(request))

def registration(request):
    context = {}
    context.update(csrf(request))
    context['languages'] = conf.LANGUAGES
    context['related_lectures'] = get_related_lectures(request)
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
                if User.objects.filter(username=username).exists() or username == '':
                    context['registration_error'] = 'Error: Username cannot be used.'
                elif User.objects.filter(email=email).exists() or email == '':
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

def check_if_login(request):
    if request.method == 'POST':
        if 'login' == request.POST['type']:
            if request.user.is_authenticated():
                return 'You are already logged in.'
            else:
                if not auth(request):
                    return 'Incorrect username or password.'

def get_lectures(course):
    lectures = []
    lectures = Lecture.objects.filter(course=course).order_by('number')
    return lectures

def get_related_lectures(request):
    if request.user.is_authenticated():
        return Lecture.objects.order_by('?')[:6]
    else:
        return Lecture.objects.order_by('?')[:6]
