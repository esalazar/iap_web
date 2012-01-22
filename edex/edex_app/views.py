from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader

from edex_app.models import Keyword
from edex_app.models import Profile
from edex_app.models import Institution
from edex_app.models import Class
from edex_app.models import Lecture
from edex_app.models import Note
from edex_app.models import Question
from edex_app.models import Answer

def index(request):
    return render_to_response('index.html', {})

def lecture(request):
    return HttpResponse("Lecture")

def search(request):
    return HttpResponse("Search")

def notes(request):
    return HttpResponse("Notes")

def profile(request):
    return HttpResponse("profile")

def register(username, first_name, last_name, email, password, language):
    pass
