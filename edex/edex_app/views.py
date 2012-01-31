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
import datetime
import json
import urllib, urllib2

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
    context['languages'] = conf.LANGUAGES
    try:
        context['related_lectures'] = get_related_lectures(request)
        context['course'] = Course.objects.get(pk=course_pk)
        context['lectures'] = get_lectures(context['course'])
        context['lecture_num'] = int(lecture_num)
        current_lecture = Lecture.objects.get(course=context['course'], number=lecture_num)
        context['lecture_pk'] = current_lecture.pk
        context['lecture_video_id'] = current_lecture.video
        questions_answers = []
        questions = Question.objects.order_by('up_votes').filter(lecture=current_lecture)
        for question in questions:
            questions_answers.append((question, Answer.objects.filter(question=question)))
        context['questions_answers'] = questions_answers
        try:
            context['notes'] = Note.objects.get(user=request.user, lecture=current_lecture)
            context['community_notes'] = Note.objects.filter(lecture=current_lecture).exclude(user=request.user)
        except:
            context['notes'] = None
            context['community_notes'] = None
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
        user_profile = Profile.objects.get(user=user)
        context['user_profile'] = user_profile
    except:
        raise Http404('Cannot find user ' + username + ".")
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

def ask_question(request):
    pass

def answer_question(request):
    if request.user.is_authenticated():
        text = request.POST['text']
        question_pk = request.POST['question_pk']
        question = Question.objects.get(pk=int(question_pk))
        answer = Answer(text=text, question=question, user=request.user, up_votes=0, down_votes=0)
        answer.save()
        return redirect('edex_app.views.lecture', course_pk=question.lecture.course.pk, lecture_num=question.lecture.number)

def ask_question(request):
    if request.user.is_authenticated():
        text = request.POST['text']
        lecture_pk = request.POST['lecture_pk']
        lecture = Lecture.objects.get(pk=int(lecture_pk))
        question = Question(text=text, lecture=lecture, user=request.user, up_votes=0, down_votes=0)
        question.save()
        return redirect('edex_app.views.lecture', course_pk=lecture.course.pk, lecture_num=lecture.number)

def save_notes(request):
    if request.user.is_authenticated():
        note = request.POST['note']
        lecture_pk = request.POST['lecture_pk']
        lecture = Lecture.objects.get(pk=int(lecture_pk))
        data = None
        try:
            note_object = Note.objects.get(user=request.user, lecture=lecture)
            note_object.text = note
            note_object.save()
        except:
            note_object = Note(user=request.user, lecture=lecture, text=note)
            note_object.save()
        finally:
            data = json.dumps({'message':'Saved at ' + datetime.datetime.now().ctime()})
    return HttpResponse(data, mimetype='applicaiton/json')

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

def translate(request):
    to = request.GET['to']
    text = urllib.quote(request.GET['text'].strip())
    url_to_bing = 'http://api.microsofttranslator.com/v2/Ajax.svc/Translate?appId=290717C1C08FFAE2540D5B8D489CFA8C0B9885DE&from=&to=' + to + '&text=' + text
    req = urllib2.urlopen(url_to_bing)
    data_from_bing = req.read()
    data = json.dumps({ 'translated': data_from_bing })
    return HttpResponse(data, mimetype='application/json')
