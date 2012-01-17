from django.http import HttpResponse
from django.template import Context, loader

from models import Keyword
from models import User_Profile
from models import Video_Profile

def index(request):
    return HttpResponse("EdEx")

def lecture(request):
    return HttpResponse("Lecture")

def search(request):
    return HttpResponse("Search")

def notes(request):
    return HttpResponse("Notes")

def profile(request):
    return HttpResponse("profile")
